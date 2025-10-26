# YouTube Music Downloader - "MusicGrab Pro"
# Complete Flask backend with React frontend

import os
import json
import subprocess
import sys
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import threading
import time
import re
import requests
from urllib.parse import quote
import urllib.parse
import base64
import tempfile
import signal
import yt_dlp

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Create directories with absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs('/home/akiva/pyytm/user_data', exist_ok=True)

# Storage - will be loaded from user data
songs_db = []
artists_db = {}
search_history = []
browser_json_content = ""
user_authenticated = False

# Load user data at startup
def load_user_data():
    """Load user data from files"""
    global songs_db, artists_db, search_history
    
    try:
        if os.path.exists('/home/akiva/pyytm/user_data/songs.json'):
            with open('/home/akiva/pyytm/user_data/songs.json', 'r') as f:
                songs_db = json.load(f)
        
        if os.path.exists('/home/akiva/pyytm/user_data/artists.json'):
            with open('/home/akiva/pyytm/user_data/artists.json', 'r') as f:
                artists_db = json.load(f)
                
        if os.path.exists('/home/akiva/pyytm/user_data/search_history.json'):
            with open('/home/akiva/pyytm/user_data/search_history.json', 'r') as f:
                search_history = json.load(f)
                
        print("✅ User data loaded successfully")
    except Exception as e:
        print(f"⚠️ Could not load user data: {e}")

def save_user_data():
    """Save user data to files"""
    try:
        with open('/home/akiva/pyytm/user_data/songs.json', 'w') as f:
            json.dump(songs_db, f)
            
        with open('/home/akiva/pyytm/user_data/artists.json', 'w') as f:
            json.dump(artists_db, f)
            
        with open('/home/akiva/pyytm/user_data/search_history.json', 'w') as f:
            json.dump(search_history, f)
            
        print("💾 User data saved")
    except Exception as e:
        print(f"⚠️ Could not save user data: {e}")

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def get_youtube_suggestions(query):
    if not query or len(query) < 1:
        return []

    url = "https://suggestqueries.google.com/complete/search"
    params = {"client": "youtube", "ds": "yt", "q": query, "hl": "en"}

    try:
        response = requests.get(url, params=params, timeout=1.0)
        text = response.text
        start = text.find('[')
        end = text.rfind(']')
        if start == -1 or end == -1:
            return []
        json_text = text[start:end+1]
        data = json.loads(json_text)
        suggestions = [item[0] for item in data[1]] if len(data) > 1 else []
        return suggestions[:5]
    except:
        return []

def parse_view_count(view_str):
    """Parse view count string into integer - IMPROVED"""
    if not view_str:
        return 0
    
    try:
        # Clean the string
        view_str = str(view_str).strip().upper().replace(',', '').replace(' ', '')
        
        # Handle "No views" or empty
        if not view_str or view_str in ['', 'NO VIEWS']:
            return 0
            
        # Handle numeric strings
        if view_str.isdigit():
            return int(view_str)
        
        # Handle formatted numbers (1.2K, 3.4M, 5.6B)
        multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000}
        
        for suffix, multiplier in multipliers.items():
            if suffix in view_str:
                # Extract the number part including decimals
                num_part = re.sub(r'[^\d.]', '', view_str)
                if num_part:
                    return int(float(num_part) * multiplier)
        
        # If no multiplier found, try to extract just numbers
        numbers_only = re.sub(r'[^\d]', '', view_str)
        return int(numbers_only) if numbers_only else 0
        
    except Exception as e:
        print(f"View count parsing error for '{view_str}': {e}")
        return 0

def get_personalized_recommendations():
    """Get personalized recommendations using browser.json"""
    global browser_json_content, user_authenticated
    
    if not user_authenticated or not browser_json_content:
        return get_popular_recommendations()
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(browser_json_content)
            browser_file = f.name
        
        from ytmusicapi import YTMusic
        ytmusic = YTMusic(browser_file)
        
        home_feed = ytmusic.get_home()
        recommendations = []
        
        for shelf in home_feed[:8]:
            for content in shelf.get('contents', [])[:6]:
                if 'title' in content:
                    video_id = content.get('videoId')
                    if video_id:
                        recommendations.append({
                            'id': video_id,
                            'title': content['title'],
                            'artist': content.get('subtitle', 'YouTube Music'),
                            'thumbnail': content['thumbnails'][-1]['url'] if content.get('thumbnails') else "",
                            'type': 'song',
                            'url': f"https://www.youtube.com/watch?v={video_id}",
                            'views': 'Popular'
                        })
        
        os.unlink(browser_file)
        return recommendations[:20]
        
    except Exception as e:
        print(f"Personalized recommendations error: {e}")
        return get_popular_recommendations()

def get_popular_recommendations():
    """Get popular music when not authenticated - FIXED"""
    try:
        from ytmusicapi import YTMusic
        yt = YTMusic()
        
        charts = yt.get_charts(country='US') or {}
        recommendations = []
        
        charts_list = charts.get('charts', [])
        if not charts_list:
            return get_fallback_recommendations()
            
        songs_chart = None
        for chart in charts_list:
            if chart.get('title') in ['Top songs', 'Trending']:
                songs_chart = chart
                break
        
        if songs_chart:
            items = songs_chart.get('items', [])
            for track in items[:12]:
                try:
                    video_id = track.get('videoId')
                    if video_id:
                        artists_list = track.get('artists', [])
                        artist_names = []
                        for artist in artists_list:
                            if isinstance(artist, dict) and 'name' in artist:
                                artist_names.append(artist['name'])
                        
                        artist_str = ", ".join(artist_names) if artist_names else 'Unknown Artist'
                        
                        thumbnails = track.get('thumbnails', [])
                        thumbnail_url = ""
                        if thumbnails:
                            thumbnail_url = thumbnails[-1].get('url', '') if len(thumbnails) > 1 else thumbnails[0].get('url', '')
                        
                        recommendations.append({
                            'id': video_id,
                            'title': track.get('title', 'Unknown Track'),
                            'artist': artist_str,
                            'thumbnail': thumbnail_url,
                            'type': 'song',
                            'url': f"https://www.youtube.com/watch?v={video_id}",
                            'views': 'Popular'
                        })
                except Exception as track_e:
                    print(f"Track parsing error: {track_e}")
                    continue
        else:
            print("⚠️ No 'Top songs' or 'Trending' chart found")
        
        return recommendations[:12] if recommendations else get_fallback_recommendations()
    except Exception as e:
        print(f"Popular recommendations error: {e}")
        return get_fallback_recommendations()

def get_fallback_recommendations():
    return [
        {'id': '1', 'title': 'Today\'s Top Hits', 'artist': 'Various Artists', 'thumbnail': '', 'type': 'playlist', 'url': '', 'views': 'Popular'},
        {'id': '2', 'title': 'Pop Rising', 'artist': 'Popular Pop Music', 'thumbnail': '', 'type': 'playlist', 'url': '', 'views': 'Trending'},
        {'id': '3', 'title': 'RapCaviar', 'artist': 'Hip Hop & Rap', 'thumbnail': '', 'type': 'playlist', 'url': '', 'views': 'Popular'},
        {'id': '4', 'title': 'Mood Booster', 'artist': 'Feel Good Hits', 'thumbnail': '', 'type': 'playlist', 'url': '', 'views': 'Popular'}
    ]

def fast_youtube_search(query, max_results=10):
    print(f"🔍 FAST Searching for: '{query}'")
    if not query:
        return {'songs': [], 'artists': [], 'albums': []}

    try:
        from ytmusicapi import YTMusic
        yt = YTMusic()
        
        songs = []
        artists = []
        albums = []
        
        try:
            # Search for songs
            songs_results = yt.search(query, filter='songs', limit=max_results)
            print(f"✅ Found {len(songs_results)} songs")
            
            for song in songs_results:
                try:
                    video_id = song.get('videoId', '')
                    song_artists = song.get('artists', [])
                    artists_str = ", ".join([artist.get('name', 'Unknown') for artist in song_artists]) if song_artists else 'Unknown Artist'
                    
                    thumbnail_url = ""
                    if song.get('thumbnails'):
                        thumbnail_url = song['thumbnails'][-1]['url'] if len(song['thumbnails']) > 1 else song['thumbnails'][0]['url']
                    
                    # Get view count - FIXED
                    raw_views = song.get('views')
                    views = parse_view_count(raw_views) if raw_views else 0
                    
                    songs.append({
                        'id': video_id,
                        'title': song.get('title', 'Unknown Title'),
                        'url': f"https://www.youtube.com/watch?v={video_id}" if video_id else '',
                        'duration': song.get('duration', '0:00'),
                        'artist': artists_str,
                        'album': song.get('album', {}).get('name', '') if song.get('album') else '',
                        'thumbnail': thumbnail_url,
                        'views': format_views(views),
                        'is_explicit': any(word in song.get('title', '').lower() for word in ['explicit', 'clean']),
                        'raw_views': views
                    })
                except Exception as song_error:
                    print(f"⚠️ Error processing song: {song_error}")
                    continue
                    
        except Exception as songs_error:
            print(f"❌ Songs search failed: {songs_error}")
        
        try:
            artists_results = yt.search(query, filter='artists', limit=4)
            print(f"✅ Found {len(artists_results)} artists")
            
            for artist in artists_results:
                try:
                    artists.append({
                        'id': artist.get('browseId', ''),
                        'name': artist.get('artist', 'Unknown Artist'),
                        'thumbnail': artist['thumbnails'][-1]['url'] if artist.get('thumbnails') else "",
                        'type': 'artist'
                    })
                except Exception as artist_error:
                    print(f"⚠️ Error processing artist: {artist_error}")
                    continue
                    
        except Exception as artists_error:
            print(f"❌ Artists search failed: {artists_error}")
        
        try:
            albums_results = yt.search(query, filter='albums', limit=4)
            print(f"✅ Found {len(albums_results)} albums")
            
            for album in albums_results:
                try:
                    albums.append({
                        'id': album.get('browseId', ''),
                        'title': album.get('title', 'Unknown Album'),
                        'artist': album.get('artists', [{}])[0].get('name', '') if album.get('artists') else 'Unknown Artist',
                        'year': album.get('year', ''),
                        'thumbnail': album['thumbnails'][-1]['url'] if album.get('thumbnails') else "",
                        'type': 'album'
                    })
                except Exception as album_error:
                    print(f"⚠️ Error processing album: {album_error}")
                    continue
                    
        except Exception as albums_error:
            print(f"❌ Albums search failed: {albums_error}")
        
        print(f"🎯 FAST Search complete: {len(songs)} songs, {len(artists)} artists, {len(albums)} albums")
        return {
            'songs': songs,
            'artists': artists,
            'albums': albums
        }
        
    except Exception as e:
        print(f"❌ Search function failed completely: {e}")
        return {'songs': [], 'artists': [], 'albums': []}

def add_metadata_to_file(filepath, title, artist, album, thumbnail_url=None):
    """Add metadata to downloaded MP3 file - FIXED"""
    try:
        from mutagen import File
        from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC
        
        # Ensure file exists
        if not os.path.exists(filepath):
            print(f"⚠️ File not found for metadata: {filepath}")
            return
        
        try:
            audio = ID3(filepath)
        except:
            audio = ID3()
        
        # Add basic metadata
        audio["TIT2"] = TIT2(encoding=3, text=title)
        audio["TPE1"] = TPE1(encoding=3, text=artist)
        if album:
            audio["TALB"] = TALB(encoding=3, text=album)
        
        # Add album art if available
        if thumbnail_url:
            try:
                response = requests.get(thumbnail_url, timeout=10)
                if response.status_code == 200:
                    # Remove existing APIC frames
                    for key in list(audio.keys()):
                        if key.startswith('APIC'):
                            del audio[key]
                    
                    audio["APIC"] = APIC(
                        encoding=3,
                        mime='image/jpeg',
                        type=3,  # 3 is for album art
                        desc='Cover',
                        data=response.content
                    )
                    print(f"✅ Added thumbnail to: {filepath}")
            except Exception as e:
                print(f"⚠️ Could not add thumbnail from URL: {e}")
        
        audio.save(filepath)
        print(f"✅ Metadata added to: {filepath}")
        
    except Exception as e:
        print(f"⚠️ Metadata error: {e}")

# Load user data at startup
load_user_data()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/home')
def home():
    """Homepage with personalized recommendations"""
    try:
        recommendations = get_personalized_recommendations()
        featured = [
            {'id': 'top-charts', 'title': 'Top Charts', 'subtitle': 'Global hits', 'type': 'chart', 'icon': 'fas fa-chart-line', 'color': 'from-purple-500 to-pink-500'},
            {'id': 'new-releases', 'title': 'New Releases', 'subtitle': 'Fresh music', 'type': 'new', 'icon': 'fas fa-star', 'color': 'from-blue-500 to-cyan-500'},
            {'id': 'mood-mixes', 'title': 'Mood Mixes', 'subtitle': 'Perfect vibes', 'type': 'mix', 'icon': 'fas fa-random', 'color': 'from-green-500 to-emerald-500'},
            {'id': 'trending', 'title': 'Trending Now', 'subtitle': 'Going viral', 'type': 'trending', 'icon': 'fas fa-fire', 'color': 'from-orange-500 to-red-500'}
        ]
        
        return jsonify({
            'recommendations': recommendations,
            'featured': featured,
            'authenticated': user_authenticated
        })
    except Exception as e:
        return jsonify({
            'recommendations': get_fallback_recommendations(),
            'featured': [],
            'authenticated': False
        })

@app.route('/api/search', methods=['POST'])
def search():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
        
    query = data.get('query', '').strip()
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    try:
        print(f"🔍 API Search called for: '{query}'")
        results = fast_youtube_search(query, 10)
        print(f"✅ API Search completed for: '{query}'")
        return jsonify(results)
    except Exception as e:
        print(f"❌ API Search failed for '{query}': {e}")
        return jsonify({'error': f'Search failed: {str(e)}'}), 500

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

    # Clean filename
    sanitized_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).strip()
    sanitized_artist = "".join(c for c in artist if c.isalnum() or c in (" ", "-", "_")).strip()
    filename = f"{sanitized_artist} - {sanitized_title}.mp3"
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

    # ULTRA-FAST download settings
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': file_path.replace('.mp3', '.%(ext)s'),
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
            {  # ADD THIS for thumbnail embedding
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            },
            {  # ADD THIS for thumbnail
                'key': 'EmbedThumbnail',
                'already_have_thumbnail': False,
            }
        ],
        'writethumbnail': True,  # Download thumbnail
        'embedthumbnail': True,  # Embed in file
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'no_check_certificate': True,
        'prefer_ffmpeg': True,
        'keepvideo': False,
        
        # SPEED OPTIMIZATIONS
        'retries': 2,
        'fragment_retries': 2,
        'skip_unavailable_fragments': True,
        'extract_flat': False,
        'concurrent_fragment_downloads': 3,  # Parallel downloads
    }

    try:
        print(f"🚀 Starting FAST download for: {title}")
        start_time = time.time()
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
        
        download_time = time.time() - start_time
        print(f"✅ Downloaded {filename} in {download_time:.1f} seconds")

        # Force metadata update
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

@app.route('/api/songs')
def get_songs():
    return jsonify({'songs': songs_db})

@app.route('/api/artists')
def get_artists():
    return jsonify({'artists': artists_db})

@app.route('/downloads/<filename>')
def serve_download(filename):
    """Serve temporary download file"""
    filepath = os.path.join('/home/akiva/pyytm/downloads', filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(filepath, as_attachment=True, download_name=filename)

@app.route('/api/play-song/<song_id>')
def play_song(song_id):
    """Serve song file for playback"""
    song = next((s for s in songs_db if s['id'] == song_id), None)
    if not song:
        return jsonify({'error': 'Song not found'}), 404
        
    filepath = os.path.join('/home/akiva/pyytm/downloads', song['filename'])
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
        
    return send_file(filepath)

@app.route('/api/download-file/<song_id>')
def download_file(song_id):
    """Download song to computer"""
    song = next((s for s in songs_db if s['id'] == song_id), None)
    if not song:
        return jsonify({'error': 'Song not found'}), 404
        
    filepath = os.path.join('/home/akiva/pyytm/downloads', song['filename'])
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
        
    download_name = f"{sanitize_filename(song['artist'])} - {sanitize_filename(song['title'])}.mp3"
    
    return send_file(filepath, as_attachment=True, download_name=download_name)

def format_views(views):
    if not views or views == 0:
        return "No views"
    
    try:
        views = int(views)
    except:
        return "No views"
        
    if views >= 1000000000:
        return f"{views / 1000000000:.1f}B views"
    elif views >= 1000000:
        return f"{views / 1000000:.1f}M views"
    elif views >= 1000:
        return f"{views / 1000:.1f}K views"
    else:
        return f"{views:,} views"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
