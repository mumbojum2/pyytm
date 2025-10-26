# YouTube Music Downloader - "MusicGrab Pro"
# Complete Flask backend with React frontend
# main.py

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

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Create directories
os.makedirs('downloads', exist_ok=True)
os.makedirs('user_data', exist_ok=True)

# Storage - will be loaded from user data
songs_db = []
artists_db = {}
search_history = []
browser_json_content = ""
user_authenticated = False

def install_dependencies():
    """Install required dependencies"""
    print("🔍 Checking dependencies...")
    
    dependencies = ['yt-dlp', 'flask', 'flask-cors', 'requests', 'ytmusicapi', 'mutagen']
    
    for package in dependencies:
        try:
            if package == 'yt-dlp':
                __import__('yt_dlp')
            elif package == 'ytmusicapi':
                __import__('ytmusicapi')
            elif package == 'mutagen':
                __import__('mutagen')
            else:
                __import__(package.replace('-', '_'))
            print(f"✅ {package} installed")
        except ImportError:
            print(f"📦 Installing {package}...")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", package],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(f"✅ {package} installed successfully")
            except Exception as e:
                print(f"❌ Failed to install {package}: {e}")

    # Upgrade yt-dlp to latest for bot detection fixes
    print("🔄 Upgrading yt-dlp...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("✅ yt-dlp upgraded")
    except Exception as e:
        print(f"⚠️ yt-dlp upgrade failed: {e}")

    # Install ffmpeg
    print("🔧 Installing ffmpeg...")
    try:
        subprocess.run(['apt-get', 'update'], check=False, capture_output=True)
        subprocess.run(['apt-get', 'install', '-y', 'ffmpeg'], check=False, capture_output=True)
        print("✅ ffmpeg installed")
    except Exception as e:
        print(f"⚠️ ffmpeg issues: {e}")

install_dependencies()

# Load user data at startup
def load_user_data():
    """Load user data from files"""
    global songs_db, artists_db, search_history
    
    try:
        if os.path.exists('user_data/songs.json'):
            with open('user_data/songs.json', 'r') as f:
                songs_db = json.load(f)
        
        if os.path.exists('user_data/artists.json'):
            with open('user_data/artists.json', 'r') as f:
                artists_db = json.load(f)
                
        if os.path.exists('user_data/search_history.json'):
            with open('user_data/search_history.json', 'r') as f:
                search_history = json.load(f)
                
        print("✅ User data loaded successfully")
    except Exception as e:
        print(f"⚠️ Could not load user data: {e}")

def save_user_data():
    """Save user data to files"""
    try:
        with open('user_data/songs.json', 'w') as f:
            json.dump(songs_db, f)
            
        with open('user_data/artists.json', 'w') as f:
            json.dump(artists_db, f)
            
        with open('user_data/search_history.json', 'w') as f:
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
    """Parse view count string into integer"""
    if not view_str:
        return 0
    
    try:
        # Remove any non-numeric characters except K, M, B
        view_str = str(view_str).strip().upper()
        
        # Handle numeric strings
        if view_str.isdigit():
            return int(view_str)
        
        # Handle formatted numbers (1.2K, 3.4M, 5.6B)
        multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000}
        
        for suffix, multiplier in multipliers.items():
            if suffix in view_str:
                # Extract the number part
                num_part = re.sub(r'[^\d.]', '', view_str)
                if num_part:
                    return int(float(num_part) * multiplier)
        
        # If no multiplier found, try to extract just numbers
        numbers_only = re.sub(r'[^\d]', '', view_str)
        return int(numbers_only) if numbers_only else 0
        
    except Exception as e:
        print(f"View count parsing error: {e}")
        return 0

def get_personalized_recommendations():
    """Get personalized recommendations using browser.json"""
    global browser_json_content, user_authenticated
    
    if not user_authenticated or not browser_json_content:
        return get_popular_recommendations()
    
    try:
        # Create temporary browser.json file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(browser_json_content)
            browser_file = f.name
        
        from ytmusicapi import YTMusic
        ytmusic = YTMusic(browser_file)
        
        home_feed = ytmusic.get_home()
        recommendations = []
        
        for shelf in home_feed[:8]:  # First 8 shelves
            for content in shelf.get('contents', [])[:6]:  # First 6 items per shelf
                if 'title' in content:
                    video_id = content.get('videoId')
                    if video_id:  # Only include items with video IDs
                        recommendations.append({
                            'id': video_id,
                            'title': content['title'],
                            'artist': content.get('subtitle', 'YouTube Music'),
                            'thumbnail': content['thumbnails'][-1]['url'] if content.get('thumbnails') else "",
                            'type': 'song',
                            'url': f"https://www.youtube.com/watch?v={video_id}",
                            'views': 'Popular'
                        })
        
        # Clean up temp file
        os.unlink(browser_file)
        
        return recommendations[:20]
        
    except Exception as e:
        print(f"Personalized recommendations error: {e}")
        return get_popular_recommendations()

def get_popular_recommendations():
    """Get popular music when not authenticated"""
    try:
        from ytmusicapi import YTMusic
        yt = YTMusic()
        
        charts = yt.get_charts(country='US')
        recommendations = []
        
        for chart in charts.get('charts', []):
            if chart['title'] in ['Top songs', 'Trending']:
                for track in chart['items'][:12]:
                    try:
                        video_id = track.get('videoId')
                        if video_id:
                            recommendations.append({
                                'id': video_id,
                                'title': track['title'],
                                'artist': ", ".join([artist['name'] for artist in track.get('artists', [])]),
                                'thumbnail': track['thumbnails'][-1]['url'] if track.get('thumbnails') else "",
                                'type': 'song',
                                'url': f"https://www.youtube.com/watch?v={video_id}",
                                'views': 'Popular'
                            })
                    except:
                        continue
                break
                
        return recommendations
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

def get_library_data():
    """Get user's library data using browser.json"""
    global browser_json_content, user_authenticated
    
    if not user_authenticated or not browser_json_content:
        return {'songs': [], 'albums': [], 'artists': [], 'playlists': []}
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(browser_json_content)
            browser_file = f.name
        
        from ytmusicapi import YTMusic
        ytmusic = YTMusic(browser_file)
        
        library_data = {
            'songs': [],
            'albums': [],
            'artists': [],
            'playlists': []
        }
        
        # Get library songs
        try:
            library_songs = ytmusic.get_library_songs(limit=100)
            for song in library_songs:
                video_id = song.get('videoId')
                if video_id:
                    library_data['songs'].append({
                        'id': video_id,
                        'title': song['title'],
                        'artist': song['artists'][0]['name'] if song.get('artists') else 'Unknown',
                        'album': song.get('album', {}).get('name', ''),
                        'duration': song.get('duration', '0:00'),
                        'thumbnail': song['thumbnails'][-1]['url'] if song.get('thumbnails') else "",
                        'url': f"https://www.youtube.com/watch?v={video_id}",
                        'views': 'In Library'
                    })
        except Exception as e:
            print(f"Library songs error: {e}")
        
        # Get library albums
        try:
            library_albums = ytmusic.get_library_albums(limit=50)
            for album in library_albums:
                library_data['albums'].append({
                    'id': album['browseId'],
                    'title': album['title'],
                    'artist': album['artists'][0]['name'] if album.get('artists') else 'Unknown',
                    'year': album.get('year', ''),
                    'thumbnail': album['thumbnails'][-1]['url'] if album.get('thumbnails') else ""
                })
        except Exception as e:
            print(f"Library albums error: {e}")
        
        # Get library artists
        try:
            library_artists = ytmusic.get_library_artists(limit=50)
            for artist in library_artists:
                library_data['artists'].append({
                    'id': artist['browseId'],
                    'name': artist['artist'],
                    'thumbnail': artist['thumbnails'][-1]['url'] if artist.get('thumbnails') else ""
                })
        except Exception as e:
            print(f"Library artists error: {e}")
        
        # Get library playlists
        try:
            library_playlists = ytmusic.get_library_playlists(limit=50)
            for playlist in library_playlists:
                library_data['playlists'].append({
                    'id': playlist['playlistId'],
                    'title': playlist['title'],
                    'count': playlist.get('count', '0'),
                    'thumbnail': playlist['thumbnails'][-1]['url'] if playlist.get('thumbnails') else ""
                })
        except Exception as e:
            print(f"Library playlists error: {e}")
        
        os.unlink(browser_file)
        return library_data
        
    except Exception as e:
        print(f"Library data error: {e}")
        return {'songs': [], 'albums': [], 'artists': [], 'playlists': []}

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
            # Search for songs - NO VIEW COUNT FETCHING FOR SPEED
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
                    
                    # Use view count from search results if available, otherwise skip
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

def get_artist_songs(artist_id):
    try:
        from ytmusicapi import YTMusic
        yt = YTMusic()
        
        artist_info = yt.get_artist(artist_id)
        
        # Get artist albums
        artist_albums = yt.get_artist_albums(artist_id)
        
        songs = []
        for album in artist_albums[:5]:  # Limit to 5 albums
            try:
                album_details = yt.get_album(album['browseId'])
                for track in album_details['tracks']:
                    video_id = track.get('videoId')
                    
                    songs.append({
                        'id': video_id,
                        'title': track['title'],
                        'duration': track.get('duration', '0:00'),
                        'album': album['title'],
                        'thumbnail': track['thumbnails'][0]['url'] if track.get('thumbnails') else "",
                        'url': f"https://www.youtube.com/watch?v={video_id}" if video_id else "",
                        'views': 'Album Track'
                    })
            except Exception as album_error:
                print(f"Album error: {album_error}")
                continue
        
        return {
            'artist': artist_info.get('name', 'Unknown Artist'),
            'description': artist_info.get('description', ''),
            'thumbnail': artist_info['thumbnails'][-1]['url'] if artist_info.get('thumbnails') else "",
            'songs': songs[:20]  # Limit to 20 songs
        }
    except Exception as e:
        print(f"Artist songs error: {e}")
        return {'artist': 'Unknown', 'description': '', 'thumbnail': '', 'songs': []}

def add_metadata_to_file(filepath, title, artist, album, thumbnail_url=None):
    """Add metadata to downloaded MP3 file"""
    try:
        from mutagen import File
        from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC
        
        audio = ID3(filepath)
        
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
                    audio["APIC"] = APIC(
                        encoding=3,
                        mime='image/jpeg',
                        type=3,  # 3 is for album art
                        desc='Cover',
                        data=response.content
                    )
            except:
                pass
        
        audio.save()
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

@app.route('/api/library')
def get_library():
    """Get user's YouTube Music library"""
    try:
        library_data = get_library_data()
        return jsonify({
            'library': library_data,
            'authenticated': user_authenticated
        })
    except Exception as e:
        return jsonify({
            'library': {'songs': [], 'albums': [], 'artists': [], 'playlists': []},
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
        import traceback
        print(f"📋 Full traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Search failed: {str(e)}'}), 500

@app.route('/api/artist/<artist_id>')
def artist_songs(artist_id):
    try:
        artist_data = get_artist_songs(artist_id)
        return jsonify(artist_data)
    except Exception as e:
        return jsonify({'error': f'Artist not found: {str(e)}'}), 500

@app.route('/api/suggestions', methods=['POST'])
def suggestions():
    data = request.get_json()
    if not data:
        return jsonify({'suggestions': []})
    query = data.get('query', '').strip()
    if len(query) < 1:
        return jsonify({'suggestions': []})
    try:
        suggestions_list = get_youtube_suggestions(query)
        return jsonify({'suggestions': suggestions_list[:5]})
    except:
        return jsonify({'suggestions': []})

@app.route('/api/search-history')
def get_search_history():
    """Get user's search history"""
    return jsonify({'history': search_history[:10]})

@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    """Authenticate with browser.json"""
    global browser_json_content, user_authenticated
    
    try:
        data = request.get_json()
        if not data or 'browserJson' not in data:
            return jsonify({'error': 'No browser.json data provided'}), 400
        
        browser_json_content = data['browserJson']
        
        # Test authentication with a simpler method
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(browser_json_content)
            browser_file = f.name
        
        from ytmusicapi import YTMusic
        ytmusic = YTMusic(browser_file)
        
        # Use a more reliable test - get account info
        try:
            account_info = ytmusic.get_account_info()
            user_authenticated = True
            return jsonify({
                'success': True, 
                'message': 'Authentication successful!',
                'account': account_info.get('name', 'Unknown')
            })
        except Exception as auth_error:
            # Fallback: try to get home feed
            try:
                ytmusic.get_home(limit=1)
                user_authenticated = True
                return jsonify({'success': True, 'message': 'Authentication successful!'})
            except:
                raise auth_error
        
        os.unlink(browser_file)
        
    except Exception as e:
        user_authenticated = False
        print(f"Authentication error: {e}")
        return jsonify({'error': f'Authentication failed: {str(e)}'}), 400

@app.route('/api/export-data')
def export_user_data():
    """Export all user data as a downloadable file"""
    try:
        export_data = {
            'songs': songs_db,
            'artists': artists_db,
            'search_history': search_history,
            'exported_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        export_filename = f"musicgrab_backup_{time.strftime('%Y%m%d_%H%M%S')}.json"
        export_path = os.path.join('user_data', export_filename)
        
        with open(export_path, 'w') as f:
            json.dump(export_data, f)
        
        return send_file(export_path, as_attachment=True, download_name=export_filename)
        
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 500

@app.route('/api/import-data', methods=['POST'])
def import_user_data():
    """Import user data from backup file"""
    global songs_db, artists_db, search_history
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and file.filename.endswith('.json'):
            import_data = json.load(file)
            
            songs_db = import_data.get('songs', [])
            artists_db = import_data.get('artists', {})
            search_history = import_data.get('search_history', [])
            
            save_user_data()
            
            return jsonify({'success': True, 'message': 'Data imported successfully!'})
        else:
            return jsonify({'error': 'Invalid file format. Please upload a JSON file.'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Import failed: {str(e)}'}), 500

@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
        
    url = data.get('url', '')
    title = data.get('title', 'Unknown')
    artist = data.get('artist', 'Unknown')
    album = data.get('album', '')
    thumbnail = data.get('thumbnail', '')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        print(f"🔄 Starting download: {title} by {artist}")
        
        # Create safe filename
        safe_title = sanitize_filename(title)
        safe_artist = sanitize_filename(artist)
        filename = f"{safe_artist} - {safe_title}" if safe_artist != "Unknown" else safe_title
        filename = filename[:100]
        
        # Download directly as MP3 with proper filename
        output_template = os.path.join('downloads', f'{filename}.%(ext)s')  # Use .%(ext)s for flexibility
        
        # Base evasion options (always include)
        evasion_opts = [
            '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.7390.123 Safari/537.36',  # Latest Chrome UA (Oct 2025)
            '--referer', 'https://www.youtube.com/',  # Mimic browser referral
        ]
        
        # Base command with format selection and evasion
        cmd = [
            sys.executable, '-m', 'yt_dlp',
            '-f', 'bestaudio',  # Auto-pick best available audio format
            '-x', '--audio-format', 'mp3',
            '--audio-quality', '0',  # Best quality during conversion
            '--add-metadata',
            '--embed-thumbnail',
            '--parse-metadata', 'title:%(title)s',
            '--parse-metadata', 'uploader:%(artist)s',
            '-o', output_template,
            '--no-warnings',
            '--sleep-interval', '5',  # Rate limit
            '--max-sleep-interval', '10',
            '--extractor-args', 'youtube:player_client=ios',  # iOS client bypass
            url
        ] + evasion_opts  # Add UA and referer

        attempts = 0
        max_attempts = 2  # Cookies -> No cookies
        final_error = None
        
        while attempts < max_attempts:
            # Add cookies if file exists and first attempt
            if attempts == 0 and os.path.exists('cookies.txt'):
                cmd_with_cookies = cmd + ['--cookies', 'cookies.txt']
                print("🔑 Using cookies for auth")
                current_cmd = cmd_with_cookies
            else:
                print(f"⚠️ Attempt {attempts + 1}: No cookies")
                current_cmd = cmd[:]  # Copy base without cookies
                
            print(f"📥 Running download command (attempt {attempts + 1})...")
            result = subprocess.run(current_cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"✅ Download completed for: {title}")
                time.sleep(2)  # Longer sleep for processing
                
                # Find the downloaded file
                possible_files = [f"{filename}.mp3", f"{filename}.m4a", f"{filename}.webm"]
                filepath = None
                for possible in possible_files:
                    test_path = os.path.join('downloads', possible)
                    if os.path.exists(test_path):
                        filepath = test_path
                        print(f"📁 Found file: {possible}")
                        break
                
                if filepath:
                    # Ensure MP3 via FFmpeg if needed
                    if not filepath.endswith('.mp3'):
                        mp3_path = filepath.rsplit('.', 1)[0] + '.mp3'
                        ffmpeg_cmd = ['ffmpeg', '-y', '-i', filepath, '-codec:a', 'libmp3lame', '-qscale:a', '0', mp3_path]
                        ff_result = subprocess.run(ffmpeg_cmd, capture_output=True)
                        if ff_result.returncode == 0 and os.path.exists(mp3_path):
                            filepath = mp3_path
                            os.remove(filepath)  # Clean up original
                            print(f"🔄 Converted to MP3: {mp3_path}")
                        else:
                            print(f"⚠️ FFmpeg conversion failed: {ff_result.stderr}")
                    
                    # Add metadata
                    add_metadata_to_file(filepath, title, artist, album, thumbnail)
                    
                    # Save to DB
                    song_info = {
                        'id': len(songs_db) + 1,
                        'title': title,
                        'artist': artist,
                        'album': album,
                        'filename': os.path.basename(filepath),
                        'filepath': filepath,
                        'downloadedAt': time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    songs_db.append(song_info)
                    
                    if artist in artists_db:
                        artists_db[artist] += 1
                    else:
                        artists_db[artist] = 1
                    
                    save_user_data()
                    
                    # Send file
                    download_name = f"{safe_artist} - {safe_title}.mp3"
                    return send_file(filepath, as_attachment=True, download_name=download_name)
                
                # If no file but success, rare—retry
                attempts += 1
                continue
            else:
                error_msg = result.stderr
                print(f"❌ Attempt {attempts + 1} failed: {error_msg[:200]}")
                final_error = error_msg
                if "Sign in to confirm" in error_msg:
                    attempts += 1  # Proceed to fallback
                else:
                    break  # Other error, stop
        
        # All attempts failed
        tips = []
        if "Sign in to confirm" in final_error:
            tips = [
                "1. Upload a fresh 'cookies.txt' file (export from your logged-in browser using the 'cookies.txt' extension).",
                "2. Try a VPN to change your server's IP (common on shared hosts like Koyeb).",
                "3. Wait 2-3 days and retry—YouTube flags IPs temporarily."
            ]
        return jsonify({
            'error': f'Download failed after retries: {final_error[:150]}...',
            'tips': tips
        }), 500
            
    except Exception as e:
        print(f"❌ Download error details: {e}")
        import traceback
        print(f"📋 Full traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

@app.route('/api/songs')
def get_songs():
    return jsonify({'songs': songs_db})

@app.route('/api/artists')
def get_artists():
    return jsonify({'artists': artists_db})

@app.route('/api/play-song/<int:song_id>')
def play_song(song_id):
    """Serve song file for playback"""
    song = next((s for s in songs_db if s['id'] == song_id), None)
    if not song:
        return jsonify({'error': 'Song not found'}), 404
        
    filepath = os.path.join('downloads', song['filename'])
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
        
    return send_file(filepath)

@app.route('/api/download-file/<int:song_id>')
def download_file(song_id):
    """Download song to computer"""
    song = next((s for s in songs_db if s['id'] == song_id), None)
    if not song:
        return jsonify({'error': 'Song not found'}), 404
        
    filepath = os.path.join('downloads', song['filename'])
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
        
    # Create download filename with proper extension
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




