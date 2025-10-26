import os
import json
import time
from datetime import datetime
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import yt_dlp
from ytmusicapi import YTMusic
import requests
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:8000", "https://*.ngrok-free.app"]}})  # Support Ngrok and local

# Define directories and files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads')
USER_DATA_FILE = os.path.join(BASE_DIR, 'user_data.json')
COOKIES_FILE = os.path.join(BASE_DIR, 'cookies.txt')

# Ensure download directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Initialize YTMusic
try:
    ytmusic = YTMusic(COOKIES_FILE)
except Exception as e:
    print(f"Failed to initialize YTMusic: {e}")
    ytmusic = None

# Load user data
user_data = {'songs': [], 'artists': {}, 'search_history': []}
try:
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            user_data = json.load(f)
except Exception as e:
    print(f"Failed to load user data: {e}")

def save_user_data():
    try:
        with open(USER_DATA_FILE, 'w') as f:
            json.dump(user_data, f, indent=4)
    except Exception as e:
        print(f"Failed to save user data: {e}")

def add_metadata(file_path, title, artist, album, thumbnail_url):
    try:
        audio = MP3(file_path, ID3=ID3)
        # Add ID3 tag if it doesn't exist
        try:
            audio.add_tags()
        except:
            pass
        audio.tags['TIT2'] = TIT2(encoding=3, text=title)
        audio.tags['TPE1'] = TPE1(encoding=3, text=artist)
        if album:
            audio.tags['TALB'] = TALB(encoding=3, text=album)
        # Download and embed thumbnail
        if thumbnail_url:
            response = requests.get(thumbnail_url)
            if response.status_code == 200:
                audio.tags['APIC'] = APIC(
                    encoding=3,  # UTF-8
                    mime='image/jpeg',
                    type=3,  # Cover (front)
                    desc='Cover',
                    data=response.content
                )
        audio.save()
        print(f"✅ Added metadata to {file_path}")
    except Exception as e:
        print(f"Metadata error: {e}")

@app.route('/api/home', methods=['GET'])
def home():
    try:
        recommendations = []
        featured = []
        authenticated = is_authenticated()

        if authenticated:
            recommendations = ytmusic.get_home(limit=12) or []
        else:
            recommendations = ytmusic.search(query="pop", filter="songs", limit=12) or []
            featured = [
                {
                    'id': '1', 'title': 'Explore Music', 'subtitle': 'Discover new tracks', 
                    'icon': 'fas fa-compass', 'color': 'from-blue-500 to-indigo-600'
                },
                {
                    'id': '2', 'title': 'Top Hits', 'subtitle': 'Today\'s biggest songs', 
                    'icon': 'fas fa-star', 'color': 'from-yellow-500 to-orange-600'
                },
                {
                    'id': '3', 'title': 'New Releases', 'subtitle': 'Fresh music drops', 
                    'icon': 'fas fa-fire', 'color': 'from-red-500 to-pink-600'
                },
                {
                    'id': '4', 'title': 'Your Library', 'subtitle': 'Your saved music', 
                    'icon': 'fas fa-heart', 'color': 'from-purple-500 to-pink-600'
                }
            ]

        formatted_recommendations = []
        for item in recommendations:
            try:
                artist = item.get('artists', [{}])[0].get('name', 'Unknown')
                thumbnail = item.get('thumbnails', [{}])[0].get('url', '')
                formatted_recommendations.append({
                    'id': item.get('videoId', ''),
                    'title': item.get('title', 'Unknown'),
                    'artist': artist,
                    'thumbnail': thumbnail
                })
            except (IndexError, KeyError, TypeError):
                continue  # Skip invalid items

        return jsonify({
            'recommendations': formatted_recommendations,
            'featured': featured,
            'authenticated': authenticated
        })
    except Exception as e:
        print(f"Popular recommendations error: {e}")
        return jsonify({
            'recommendations': [],
            'featured': featured,
            'authenticated': authenticated
        }), 200

@app.route('/api/songs', methods=['GET'])
def get_songs():
    return jsonify({'songs': user_data['songs']})

@app.route('/api/artists', methods=['GET'])
def get_artists():
    return jsonify({'artists': user_data['artists']})

@app.route('/api/search-history', methods=['GET'])
def get_search_history():
    return jsonify({'history': user_data['search_history']})

@app.route('/api/suggestions', methods=['POST'])
def suggestions():
    query = request.get_json().get('query', '').strip()
    if not query:
        return jsonify({'suggestions': []})
    try:
        suggestions = ytmusic.get_search_suggestions(query) if ytmusic else []
        return jsonify({'suggestions': suggestions[:10]})
    except Exception as e:
        print(f"Suggestions error: {e}")
        return jsonify({'suggestions': []})

@app.route('/api/search', methods=['POST'])
def search():
    query = request.get_json().get('query', '').strip()
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    print(f"🔍 API Search called for: '{query}'")
    try:
        print(f"🔍 FAST Searching for: '{query}'")
        search_results = ytmusic.search(query, filter='songs', limit=20) if ytmusic else []
        songs = [{
            'id': item['videoId'],
            'title': item['title'],
            'artist': item['artists'][0]['name'] if item['artists'] else 'Unknown',
            'album': item.get('album', {}).get('name', ''),
            'thumbnail': item['thumbnails'][0]['url'] if item['thumbnails'] else '',
            'duration': item.get('duration', 'Unknown'),
            'views': item.get('views', 'Unknown'),
            'is_explicit': item.get('isExplicit', False)
        } for item in search_results]
        print(f"✅ Found {len(songs)} songs")

        search_results = ytmusic.search(query, filter='artists', limit=20) if ytmusic else []
        artists = [{
            'id': item['browseId'],
            'name': item['artist'],
            'thumbnail': item['thumbnails'][0]['url'] if item['thumbnails'] else ''
        } for item in search_results]
        print(f"✅ Found {len(artists)} artists")

        search_results = ytmusic.search(query, filter='albums', limit=20) if ytmusic else []
        albums = [{
            'id': item['browseId'],
            'title': item['title'],
            'artist': item['artist'],
            'thumbnail': item['thumbnails'][0]['url'] if item['thumbnails'] else '',
            'year': item.get('year', '')
        } for item in search_results]
        print(f"✅ Found {len(albums)} albums")

        print(f"🎯 FAST Search complete: {len(songs)} songs, {len(artists)} artists, {len(albums)} albums")
        if query not in user_data['search_history']:
            user_data['search_history'] = ([query] + user_data['search_history'])[:10]
            save_user_data()
        print(f"✅ API Search completed for: '{query}'")
        return jsonify({'songs': songs, 'artists': artists, 'albums': albums})
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/artist/<artist_id>', methods=['GET'])
def artist(artist_id):
    try:
        artist_info = ytmusic.get_artist(artist_id) if ytmusic else {}
        songs = ytmusic.get_artist_songs(artist_id, limit=20) if ytmusic else []
        return jsonify({
            'artist': artist_info.get('name', 'Unknown'),
            'thumbnail': artist_info['thumbnails'][0]['url'] if artist_info.get('thumbnails') else '',
            'description': artist_info.get('description', ''),
            'songs': [{
                'id': song['videoId'],
                'title': song['title'],
                'album': song.get('album', {}).get('name', ''),
                'thumbnail': song['thumbnails'][0]['url'] if song['thumbnails'] else '',
                'duration': song.get('duration', 'Unknown'),
                'views': song.get('views', 'Unknown')
            } for song in songs]
        })
    except Exception as e:
        print(f"Artist error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json()
    video_id = data.get('videoId')
    title = data.get('title', 'Unknown')
    artist = data.get('artist', 'Unknown')
    album = data.get('album', '')
    thumbnail_url = data.get('thumbnail', '')
    format = data.get('format', 'mp3')

    if not video_id:
        return jsonify({'error': 'No videoId provided'}), 400

    sanitized_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).strip()
    sanitized_artist = "".join(c for c in artist if c.isalnum() or c in (" ", "-", "_")).strip()
    filename = f"{sanitized_artist} - {sanitized_title}_{video_id}.mp3"
    file_path = os.path.join(DOWNLOAD_DIR, filename)

    # Check if file exists (cache hit)
    if os.path.exists(file_path):
        print(f"✅ Cache hit for {filename}")
        add_metadata_to_file(file_path, title, artist, album, thumbnail_url)
        songs_db.append({
            'id': video_id,
            'title': title,
            'artist': artist,
            'album': album,
            'filename': filename,
            'thumbnail': thumbnail_url,
            'downloaded_at': time.strftime('%Y-%m-%d %H:%M:%S')
        })
        artists_db[artist] = artists_db.get(artist, 0) + 1
        save_user_data()
        return jsonify({
            'status': 'success',
            'downloadUrl': f"/downloads/{filename}",
            'filename': filename
        })

    # Download with yt-dlp
    ydl_opts = {
        'format': 'bestaudio[ext=mp3]',
        'outtmpl': file_path,
        'cookiefile': os.path.join(BASE_DIR, 'cookies.txt'),
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'noprogress': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
        print(f"✅ Downloaded {filename}")

        # Add metadata and thumbnail
        add_metadata_to_file(file_path, title, artist, album, thumbnail_url)

        # Update user data
        songs_db.append({
            'id': video_id,
            'title': title,
            'artist': artist,
            'album': album,
            'filename': filename,
            'thumbnail': thumbnail_url,
            'downloaded_at': time.strftime('%Y-%m-%d %H:%M:%S')
        })
        artists_db[artist] = artists_db.get(artist, 0) + 1
        save_user_data()

        return jsonify({
            'status': 'success',
            'downloadUrl': f"/downloads/{filename}",
            'filename': filename
        })
    except Exception as e:
        print(f"Download error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/downloads/<filename>', methods=['GET'])
def serve_download(filename):
    file_path = os.path.join(DOWNLOAD_DIR, filename)
    if os.path.exists(file_path):
        # Use client-side filename override for clean name
        return send_file(file_path, as_attachment=True, download_name=filename)
    return jsonify({'error': 'File not found'}), 404

@app.route('/api/play-song/<song_id>', methods=['GET'])
def play_song(song_id):
    for song in user_data['songs']:
        if song['id'] == song_id:
            filename = f"{song['artist']} - {song['title']}_{song_id}.mp3"
            file_path = os.path.join(DOWNLOAD_DIR, filename)
            if os.path.exists(file_path):
                return send_file(file_path, mimetype='audio/mpeg')
    return jsonify({'error': 'Song not found'}), 404

@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    browser_json = request.get_json().get('browserJson', '')
    try:
        with open('browser.json', 'w') as f:
            f.write(browser_json)
        global ytmusic
        ytmusic = YTMusic('browser.json')
        os.remove('browser.json')
        return jsonify({'success': True})
    except Exception as e:
        print(f"Authentication error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/library', methods=['GET'])
def library():
    try:
        library_data = {'songs': [], 'albums': [], 'artists': [], 'playlists': []}
        if ytmusic:
            library_songs = ytmusic.get_library_songs(limit=50)
            library_data['songs'] = [{
                'id': song['videoId'],
                'title': song['title'],
                'artist': song['artists'][0]['name'] if song['artists'] else 'Unknown',
                'album': song.get('album', {}).get('name', ''),
                'thumbnail': song['thumbnails'][0]['url'] if song['thumbnails'] else '',
                'duration': song.get('duration', 'Unknown')
            } for song in library_songs]
            library_data['artists'] = ytmusic.get_library_artists(limit=20)
            library_data['albums'] = ytmusic.get_library_albums(limit=20)
            library_data['playlists'] = ytmusic.get_library_playlists(limit=20)
        return jsonify({'library': library_data, 'authenticated': bool(ytmusic)})
    except Exception as e:
        print(f"Library error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-data', methods=['GET'])
def export_data():
    try:
        return send_file(
            USER_DATA_FILE,
            as_attachment=True,
            download_name=f"musicgrab_backup_{datetime.now().strftime('%Y-%m-%d')}.json"
        )
    except Exception as e:
        print(f"Export error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/import-data', methods=['POST'])
def import_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    try:
        global user_data
        user_data = json.load(file)
        save_user_data()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Import error: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
