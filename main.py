from flask import Flask, request, jsonify, send_file
import os
import json
import time
import subprocess
import logging
from ytmusicapi import YTMusic
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC
import yt_dlp  # Correct import
import threading
from flask_cors import CORS
import re

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Logging setup
logging.basicConfig(filename='/tmp/flask.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize YTMusic
try:
    ytmusic = YTMusic('cookies.txt')
    logger.info("✅ User data loaded successfully")
except Exception as e:
    logger.error(f"Failed to initialize YTMusic: {str(e)}")
    ytmusic = None

# Data storage
SONGS_FILE = 'songs.json'
ARTISTS_FILE = 'artists.json'
SEARCH_HISTORY_FILE = 'search_history.json'

def load_json(file_path, default):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

songs = load_json(SONGS_FILE, [])
artists = load_json(ARTISTS_FILE, {})
search_history = load_json(SEARCH_HISTORY_FILE, [])

def save_song(song_data):
    global songs
    songs.append(song_data)
    save_json(SONGS_FILE, songs)
    artist = song_data.get('artist', 'Unknown')
    artists[artist] = artists.get(artist, 0) + 1
    save_json(ARTISTS_FILE, artists)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/home')
def get_home_data():
    try:
        if ytmusic:
            home_data = ytmusic.get_home(limit=12)
            recommendations = []
            for item in home_data:
                try:
                    if 'videos' in item:
                        for video in item.get('videos', []):
                            recommendations.append({
                                'id': video.get('videoId', ''),
                                'title': video.get('title', 'Unknown'),
                                'artist': video.get('artist', 'Unknown'),
                                'thumbnail': video.get('thumbnail', {}).get('thumbnails', [{}])[-1].get('url', '')
                            })
                except (IndexError, KeyError) as e:
                    logger.error(f"Error processing home item: {str(e)}")
                    continue
            return jsonify({
                'recommendations': recommendations[:6],
                'featured': [
                    {'id': 'new', 'title': 'New Releases', 'subtitle': 'Discover new music', 'icon': 'fas fa-fire', 'color': 'from-purple-500 to-pink-500'},
                    {'id': 'charts', 'title': 'Top Charts', 'subtitle': 'Trending songs', 'icon': 'fas fa-chart-line', 'color': 'from-blue-500 to-indigo-500'},
                    {'id': 'genres', 'title': 'Genres', 'subtitle': 'Explore by mood', 'icon': 'fas fa-guitar', 'color': 'from-green-500 to-teal-500'},
                    {'id': 'playlists', 'title': 'Playlists', 'subtitle': 'Curated for you', 'icon': 'fas fa-list', 'color': 'from-red-500 to-orange-500'}
                ],
                'authenticated': bool(ytmusic)
            })
        else:
            return jsonify({'recommendations': [], 'featured': [], 'authenticated': False})
    except Exception as e:
        logger.error(f"Home data error: {str(e)}")
        return jsonify({'recommendations': [], 'featured': [], 'authenticated': False})

@app.route('/api/suggestions', methods=['POST'])
def get_suggestions():
    query = request.json.get('query', '').strip()
    if not query or not ytmusic:
        return jsonify({'suggestions': []})
    try:
        suggestions = ytmusic.get_search_suggestions(query)[:5]
        return jsonify({'suggestions': suggestions})
    except Exception as e:
        logger.error(f"Suggestions error: {str(e)}")
        return jsonify({'suggestions': []})

@app.route('/api/search', methods=['POST'])
def search():
    query = request.json.get('query', '').strip()
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    logger.info(f"🔍 API Search called for: '{query}'")
    try:
        logger.info(f"🔍 FAST Searching for: '{query}'")
        search_results = ytmusic.search(query, filter='songs', limit=20)
        songs_data = [{
            'id': item.get('videoId', ''),
            'title': item.get('title', 'Unknown'),
            'artist': item.get('artists', [{}])[0].get('name', 'Unknown'),
            'album': item.get('album', {}).get('name', ''),
            'thumbnail': item.get('thumbnails', [{}])[-1].get('url', ''),
            'duration': item.get('duration', 'Unknown'),
            'views': item.get('views', 'Unknown'),
            'is_explicit': item.get('isExplicit', False)
        } for item in search_results]
        logger.info(f"✅ Found {len(songs_data)} songs")
        
        search_results_artists = ytmusic.search(query, filter='artists', limit=20)
        artists_data = [{
            'id': item.get('artistId', ''),
            'name': item.get('artist', 'Unknown'),
            'thumbnail': item.get('thumbnails', [{}])[-1].get('url', '')
        } for item in search_results_artists]
        logger.info(f"✅ Found {len(artists_data)} artists")
        
        search_results_albums = ytmusic.search(query, filter='albums', limit=20)
        albums_data = [{
            'id': item.get('albumId', ''),
            'title': item.get('title', 'Unknown'),
            'artist': item.get('artists', [{}])[0].get('name', 'Unknown'),
            'thumbnail': item.get('thumbnails', [{}])[-1].get('url', ''),
            'year': item.get('year', '')
        } for item in search_results_albums]
        logger.info(f"✅ Found {len(albums_data)} albums")
        
        if query not in search_history:
            search_history.append(query)
            if len(search_history) > 10:
                search_history.pop(0)
            save_json(SEARCH_HISTORY_FILE, search_history)
        
        logger.info(f"🎯 FAST Search complete: {len(songs_data)} songs, {len(artists_data)} artists, {len(albums_data)} albums")
        return jsonify({
            'songs': songs_data,
            'artists': artists_data,
            'albums': albums_data
        })
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/artist/<artist_id>')
def get_artist(artist_id):
    try:
        artist_data = ytmusic.get_artist(artist_id)
        songs = [{
            'id': song.get('videoId', ''),
            'title': song.get('title', 'Unknown'),
            'album': song.get('album', {}).get('name', ''),
            'thumbnail': song.get('thumbnails', [{}])[-1].get('url', ''),
            'duration': song.get('duration', 'Unknown'),
            'views': song.get('views', 'Unknown')
        } for song in artist_data.get('songs', {}).get('results', [])]
        return jsonify({
            'artist': artist_data.get('name', 'Unknown'),
            'thumbnail': artist_data.get('thumbnails', [{}])[-1].get('url', ''),
            'description': artist_data.get('description', ''),
            'songs': songs
        })
    except Exception as e:
        logger.error(f"Artist error: {str(e)}")
        return jsonify({'error': str(e)}), 404

@app.route('/api/songs')
def get_songs():
    return jsonify({'songs': songs})

@app.route('/api/artists')
def get_artists():
    return jsonify({'artists': artists})

@app.route('/api/search-history')
def get_search_history():
    return jsonify({'history': search_history})

def add_metadata_to_file(file_path, title, artist, album, thumbnail_url):
    try:
        audio = MP3(file_path, ID3=ID3)
        if not audio.tags:
            audio.add_tags()
        
        audio.tags.add(TIT2(encoding=3, text=title))
        audio.tags.add(TPE1(encoding=3, text=artist))
        if album:
            audio.tags.add(TALB(encoding=3, text=album))
        
        if thumbnail_url:
            try:
                import requests
                response = requests.get(thumbnail_url, timeout=5)
                if response.status_code == 200:
                    audio.tags.add(APIC(
                        encoding=3,
                        mime='image/jpeg',
                        type=3,
                        desc='Cover',
                        data=response.content
                    ))
            except Exception as e:
                logger.error(f"Failed to add thumbnail: {str(e)}")
        
        audio.save()
        logger.info(f"✅ Metadata added to {file_path}")
    except Exception as e:
        logger.error(f"Metadata error: {str(e)}")

@app.route('/api/download', methods=['POST'])
def download():
    data = request.json
    video_id = data.get('videoId')
    title = data.get('title', 'Unknown')
    artist = data.get('artist', 'Unknown')
    album = data.get('album', '')
    thumbnail = data.get('thumbnail', '')
    format = data.get('format', 'mp3')

    if not video_id:
        return jsonify({'error': 'Video ID is required'}), 400

    output_dir = 'downloads'
    os.makedirs(output_dir, exist_ok=True)
    sanitized_title = re.sub(r'[<>:"/\\|?*]', '', title)
    output_file = os.path.join(output_dir, f"{sanitized_title}.{format}")

    if os.path.exists(output_file):
        logger.info(f"📂 Using cached file: {output_file}")
        song_data = {
            'id': video_id,
            'title': title,
            'artist': artist,
            'album': album,
            'thumbnail': thumbnail,
            'downloaded_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        save_song(song_data)
        return jsonify({'status': 'success', 'downloadUrl': f"/downloads/{sanitized_title}.{format}"})

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_file,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format,
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
            'noprogress': True,
            'cookiefile': 'cookies.txt',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])

        if not os.path.exists(output_file):
            return jsonify({'error': 'Download failed'}), 500

        add_metadata_to_file(output_file, title, artist, album, thumbnail)

        song_data = {
            'id': video_id,
            'title': title,
            'artist': artist,
            'album': album,
            'thumbnail': thumbnail,
            'downloaded_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        save_song(song_data)

        return jsonify({'status': 'success', 'downloadUrl': f"/downloads/{sanitized_title}.{format}"})
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/downloads/<filename>')
def serve_download(filename):
    file_path = os.path.join('downloads', filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

@app.route('/api/download-file/<song_id>')
def download_file(song_id):
    song = next((s for s in songs if s['id'] == song_id), None)
    if not song:
        return jsonify({'error': 'Song not found'}), 404

    file_path = os.path.join('downloads', f"{re.sub(r'[<>:"/\\|?*]', '', song['title'])}.mp3")
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

@app.route('/api/play-song/<song_id>')
def play_song(song_id):
    song = next((s for s in songs if s['id'] == song_id), None)
    if not song:
        return jsonify({'error': 'Song not found'}), 404

    file_path = os.path.join('downloads', f"{re.sub(r'[<>:"/\\|?*]', '', song['title'])}.mp3")
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='audio/mpeg')
    return jsonify({'error': 'File not found'}), 404

@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    data = request.json
    browser_json = data.get('browserJson', '')
    if not browser_json:
        return jsonify({'error': 'browser.json content is required'}), 400

    try:
        with open('browser.json', 'w') as f:
            f.write(browser_json)
        global ytmusic
        ytmusic = YTMusic('browser.json')
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/library')
def get_library():
    if not ytmusic:
        return jsonify({'library': {'songs': [], 'albums': [], 'artists': [], 'playlists': []}, 'authenticated': False})

    try:
        library_songs = ytmusic.get_library_songs(limit=100)
        songs_data = [{
            'id': song.get('videoId', ''),
            'title': song.get('title', 'Unknown'),
            'artist': song.get('artists', [{}])[0].get('name', 'Unknown'),
            'album': song.get('album', {}).get('name', ''),
            'thumbnail': song.get('thumbnails', [{}])[-1].get('url', ''),
            'duration': song.get('duration', 'Unknown')
        } for song in library_songs]
        
        library_artists = ytmusic.get_library_artists(limit=50)
        artists_data = [{
            'id': artist.get('artistId', ''),
            'name': artist.get('artist', 'Unknown'),
            'thumbnail': artist.get('thumbnails', [{}])[-1].get('url', '')
        } for artist in library_artists]
        
        library_albums = ytmusic.get_library_albums(limit=50)
        albums_data = [{
            'id': album.get('albumId', ''),
            'title': album.get('title', 'Unknown'),
            'artist': album.get('artists', [{}])[0].get('name', 'Unknown'),
            'thumbnail': album.get('thumbnails', [{}])[-1].get('url', ''),
            'year': album.get('year', '')
        } for album in library_albums]
        
        playlists = ytmusic.get_library_playlists(limit=50)
        playlists_data = [{
            'id': playlist.get('playlistId', ''),
            'title': playlist.get('title', 'Unknown'),
            'count': playlist.get('count', 0)
        } for playlist in playlists]
        
        return jsonify({
            'library': {
                'songs': songs_data,
                'artists': artists_data,
                'albums': albums_data,
                'playlists': playlists_data
            },
            'authenticated': True
        })
    except Exception as e:
        logger.error(f"Library error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-data')
def export_data():
    data = {
        'songs': songs,
        'artists': artists,
        'search_history': search_history
    }
    file_path = 'backup.json'
    save_json(file_path, data)
    return send_file(file_path, as_attachment=True)

@app.route('/api/import-data', methods=['POST'])
def import_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    try:
        data = json.load(file)
        global songs, artists, search_history
        songs = data.get('songs', [])
        artists = data.get('artists', {})
        search_history = data.get('search_history', [])
        save_json(SONGS_FILE, songs)
        save_json(ARTISTS_FILE, artists)
        save_json(SEARCH_HISTORY_FILE, search_history)
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Import error: {str(e)}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
