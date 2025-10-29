# YouTube Music Downloader - "MusicGrab Pro"
# ULTRA-FAST Flask Backend with Performance Optimizations

import os
import json
import subprocess
import sys
from flask import Flask, request, jsonify, send_file, Response
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

# NEW: Performance optimizations
search_cache = {}
stream_cache = {}
download_queue = []
current_downloads = 0
MAX_CONCURRENT_DOWNLOADS = 2
CACHE_DURATION = 300  # 5 minutes

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
    """Get YouTube search suggestions - OPTIMIZED FAST VERSION"""
    if not query or len(query) < 2:
        return []

    try:
        url = "https://suggestqueries.google.com/complete/search"
        params = {
            'client': 'firefox',
            'q': query,
            'hl': 'en',
            'ds': 'yt'
        }

        # OPTIMIZATION: Shorter timeout and connection pooling
        response = requests.get(url, params=params, timeout=1.5)  # Reduced from 2s to 1.5s
        
        if response.status_code == 200:
            data = response.json()
            
            if isinstance(data, list) and len(data) > 1 and isinstance(data[1], list):
                suggestions = data[1][:5]
                print(f"✅ Fast suggestions for '{query}': {suggestions}")
                return suggestions
                
    except requests.exceptions.Timeout:
        print(f"⚠️ Suggestions timeout for: {query}")
        # Return cached/fallback suggestions immediately on timeout
        return get_fallback_suggestions(query)
    except Exception as e:
        print(f"⚠️ Suggestions error for {query}: {e}")
    
    # Fast fallback
    return get_fallback_suggestions(query)

def get_fallback_suggestions(query):
    """Fast fallback suggestions without external API calls"""
    # Common music-related suggestions
    music_suggestions = [
        f"{query} songs",
        f"{query} lyrics", 
        f"{query} official video",
        f"{query} album",
        f"{query} music video",
        f"{query} live",
        f"{query} cover",
        f"{query} remix"
    ]
    return music_suggestions[:5]

def parse_view_count(view_str):
    """Parse view count string into integer - SIMPLIFIED"""
    if not view_str:
        return 0
    
    try:
        # Clean the string
        view_str = str(view_str).strip().upper().replace(',', '').replace(' ', '')
        
        # Return 0 if empty or "No views"
        if not view_str or 'NO' in view_str:
            return 0
            
        # Handle numeric strings
        if view_str.isdigit():
            return int(view_str)
        
        # Handle K, M, B suffixes
        if 'K' in view_str:
            num = float(re.sub(r'[^\d.]', '', view_str))
            return int(num * 1000)
        elif 'M' in view_str:
            num = float(re.sub(r'[^\d.]', '', view_str))
            return int(num * 1000000)
        elif 'B' in view_str:
            num = float(re.sub(r'[^\d.]', '', view_str))
            return int(num * 1000000000)
            
        # Try to extract any numbers
        numbers = re.findall(r'\d+', view_str)
        if numbers:
            return int(''.join(numbers))
            
        return 0
        
    except Exception as e:
        print(f"View count parsing error for '{view_str}': {e}")
        return 0

def format_views(views):
    """Format view count into human readable format"""
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

def get_cached_search(query):
    """Get cached search results"""
    now = time.time()
    if query in search_cache:
        data, timestamp = search_cache[query]
        if now - timestamp < CACHE_DURATION:
            return data
    return None

def cache_search(query, data):
    """Cache search results"""
    search_cache[query] = (data, time.time())

def get_personalized_recommendations():
    """Get FAST personalized recommendations"""
    global browser_json_content, user_authenticated
    
    if not user_authenticated or not browser_json_content:
        return get_fast_popular_recommendations()
    
    try:
        # Fast path with timeout
        def timeout_handler(signum, frame):
            raise TimeoutError("Recommendations timed out")
        
        # Set up timeout (Unix-like systems only)
        try:
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(5)  # 5 second timeout
        except (AttributeError, ValueError):
            # Windows doesn't support SIGALRM, continue without timeout
            pass
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                f.write(browser_json_content)
                browser_file = f.name
            
            from ytmusicapi import YTMusic
            ytmusic = YTMusic(browser_file)
            
            home_feed = ytmusic.get_home()
            recommendations = []
            
            for shelf in home_feed[:6]:  # Limit shelves for speed
                for content in shelf.get('contents', [])[:4]:  # Limit contents
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
            # Cancel timeout if set
            try:
                signal.alarm(0)
            except (AttributeError, ValueError):
                pass
            return recommendations[:15]  # Limit results
            
        except TimeoutError:
            print("Recommendations timed out, using fallback")
            return get_fast_popular_recommendations()
        
    except Exception as e:
        print(f"Personalized recommendations error: {e}")
        # Cancel timeout if set
        try:
            signal.alarm(0)
        except (AttributeError, ValueError):
            pass
        return get_fast_popular_recommendations()

def get_fast_popular_recommendations():
    """Get popular music FAST with fallback"""
    try:
        from ytmusicapi import YTMusic
        yt = YTMusic()
        
        # Direct trending search with limit
        search_results = yt.search('popular music', filter='songs', limit=8)
        recommendations = []
        
        for track in search_results[:8]:  # Limit results
            try:
                video_id = track.get('videoId')
                if video_id:
                    artists_list = track.get('artists', [])
                    artist_names = [artist.get('name', '') for artist in artists_list if isinstance(artist, dict)]
                    artist_str = ", ".join(artist_names) if artist_names else 'Unknown Artist'
                    
                    thumbnails = track.get('thumbnails', [])
                    thumbnail_url = thumbnails[-1].get('url', '') if thumbnails else ""
                    
                    recommendations.append({
                        'id': video_id,
                        'title': track.get('title', 'Unknown Track'),
                        'artist': artist_str,
                        'thumbnail': thumbnail_url,
                        'type': 'song',
                        'url': f"https://www.youtube.com/watch?v={video_id}",
                        'views': 'Popular'
                    })
            except Exception:
                continue
        
        return recommendations if recommendations else get_fallback_recommendations()
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
    print(f"🔍 ULTRA-FAST Searching for: '{query}'")
    if not query:
        return {'songs': [], 'artists': [], 'albums': []}

    try:
        from ytmusicapi import YTMusic
        yt = YTMusic()
        
        songs = []
        artists = []
        albums = []
        
        # PARALLEL searching for maximum speed
        def search_songs():
            nonlocal songs
            try:
                songs_results = yt.search(query, filter='songs', limit=max_results)
                for song in songs_results:
                    try:
                        video_id = song.get('videoId', '')
                        if not video_id:
                            continue
                            
                        song_artists = song.get('artists', [])
                        artists_str = ", ".join([artist.get('name', 'Unknown') for artist in song_artists]) if song_artists else 'Unknown Artist'
                        
                        thumbnail_url = ""
                        if song.get('thumbnails'):
                            thumbnail_url = song['thumbnails'][-1]['url'] if len(song['thumbnails']) > 1 else song['thumbnails'][0]['url']
                        
                        raw_views = song.get('views', '')
                        views = parse_view_count(raw_views)
                        
                        songs.append({
                            'id': video_id,
                            'title': song.get('title', 'Unknown Title'),
                            'url': f"https://www.youtube.com/watch?v={video_id}",
                            'duration': song.get('duration', '0:00'),
                            'artist': artists_str,
                            'album': song.get('album', {}).get('name', '') if song.get('album') else '',
                            'thumbnail': thumbnail_url,
                            'views': format_views(views),
                            'is_explicit': any(word in song.get('title', '').lower() for word in ['explicit', 'clean']),
                            'raw_views': views
                        })
                    except Exception as song_error:
                        continue
            except Exception:
                pass
        
        def search_artists():
            nonlocal artists
            try:
                artists_results = yt.search(query, filter='artists', limit=4)
                for artist in artists_results:
                    try:
                        artists.append({
                            'id': artist.get('browseId', ''),
                            'name': artist.get('artist', 'Unknown Artist'),
                            'thumbnail': artist['thumbnails'][-1]['url'] if artist.get('thumbnails') else "",
                            'type': 'artist'
                        })
                    except Exception:
                        continue
            except Exception:
                pass
        
        def search_albums():
            nonlocal albums
            try:
                albums_results = yt.search(query, filter='albums', limit=4)
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
                    except Exception:
                        continue
            except Exception:
                pass
        
        # Run searches in parallel threads
        threads = [
            threading.Thread(target=search_songs),
            threading.Thread(target=search_artists),
            threading.Thread(target=search_albums)
        ]
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join(timeout=5)  # 5 second timeout for each
        
        print(f"🎯 ULTRA-FAST Search complete: {len(songs)} songs, {len(artists)} artists, {len(albums)} albums")
        return {
            'songs': songs[:max_results],
            'artists': artists,
            'albums': albums
        }
        
    except Exception as e:
        print(f"❌ Search function failed: {e}")
        return {'songs': [], 'artists': [], 'albums': []}

def add_metadata_to_file(filepath, title, artist, album, thumbnail_url=None):
    """Add metadata to downloaded MP3 file"""
    try:
        from mutagen import File
        from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC
        
        if not os.path.exists(filepath):
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
        
        # Add album art
        if thumbnail_url:
            try:
                response = requests.get(thumbnail_url, timeout=5)  # Reduced timeout
                if response.status_code == 200:
                    # Remove existing APIC frames
                    for key in list(audio.keys()):
                        if key.startswith('APIC'):
                            del audio[key]
                    
                    audio["APIC"] = APIC(
                        encoding=3,
                        mime='image/jpeg',
                        type=3,
                        desc='Cover',
                        data=response.content
                    )
            except Exception as e:
                print(f"⚠️ Could not add thumbnail: {e}")
        
        audio.save(filepath)
        
    except Exception as e:
        print(f"⚠️ Metadata error: {e}")

def get_audio_stream_url(video_id):
    """Get direct audio stream URL for INSTANT playback - UPDATED"""
    try:
        # Updated settings for SABR streaming
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'socket_timeout': 10,
            'noplaylist': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            
            # Try multiple methods to get URL
            if 'url' in info:
                return info['url']
            elif 'formats' in info:
                # Find any working audio format
                audio_formats = [f for f in info['formats'] if f.get('vcodec') == 'none' and f.get('acodec') != 'none']
                
                if audio_formats:
                    # Just get the first working format
                    for fmt in audio_formats:
                        if fmt.get('url'):
                            return fmt['url']
            
        return None
    except Exception as e:
        print(f"Audio stream error: {e}")
        return None

# NEW: Download queue system
def process_download_queue():
    """Process download queue in background"""
    global current_downloads
    
    if not download_queue or current_downloads >= MAX_CONCURRENT_DOWNLOADS:
        return
    
    # Get next download
    download_item = download_queue.pop(0)
    current_downloads += 1
    
    # Start download in background thread
    thread = threading.Thread(target=process_single_download, args=(download_item,))
    thread.daemon = True
    thread.start()

def process_single_download(download_item):
    """Process a single download item"""
    global current_downloads
    
    try:
        # Update status to downloading
        download_item['status'] = 'downloading'
        
        # Call the download function with fast mode
        result = download_internal(
            download_item['video_id'],
            download_item['title'],
            download_item['artist'],
            download_item['album'],
            download_item['thumbnail'],
            download_item['format'],
            fast_mode=download_item.get('fast', True)
        )
        
        # Update status based on result
        if result.get('status') == 'success':
            download_item['status'] = 'completed'
            download_item['filename'] = result.get('filename')
        else:
            download_item['status'] = 'failed'
            download_item['error'] = result.get('error')
            
    except Exception as e:
        download_item['status'] = 'failed'
        download_item['error'] = str(e)
    finally:
        current_downloads -= 1
        # Process next in queue
        process_download_queue()

def download_internal(video_id, title, artist, album, thumbnail_url, format, fast_mode=False):
    """Internal download function with fast mode support"""
    # Clean filename
    sanitized_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).strip()
    sanitized_artist = "".join(c for c in artist if c.isalnum() or c in (" ", "-", "_")).strip()
    filename = f"{sanitized_artist} - {sanitized_title}.mp3"
    file_path = os.path.join(DOWNLOAD_DIR, filename)

    # Check if file exists (cache hit)
    if os.path.exists(file_path):
        print(f"✅ Cache hit for {filename}")
        # Only add metadata if not in fast mode
        if not fast_mode:
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
        return {
            'status': 'success',
            'downloadUrl': f"/downloads/{filename}",
            'filename': filename
        }

    # ULTRA-FAST download settings
    if fast_mode:
        # MINIMAL settings for maximum speed
        ydl_opts = {
            'format': 'bestaudio[filesize<50M]',  # Limit file size for speed
            'outtmpl': file_path.replace('.mp3', ''),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',  # Lower quality = faster
            }],
            'writethumbnail': False,  # Skip thumbnail
            'embedthumbnail': False,  # Skip embedding
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'nooverwrites': True,
            'noprogress': True,
            'socket_timeout': 30,
            'retries': 3,
        }
    else:
        # Standard fast settings
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio',
            'outtmpl': file_path.replace('.mp3', '.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'writethumbnail': True,
            'embedthumbnail': True,
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 30,
        }

    try:
        print(f"🚀 Starting {'FAST ' if fast_mode else ''}download for: {title}")
        start_time = time.time()
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
        
        download_time = time.time() - start_time
        print(f"✅ Downloaded {filename} in {download_time:.1f} seconds")

        # Only add metadata if not in fast mode
        if not fast_mode:
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

        return {
            'status': 'success',
            'downloadUrl': f"/downloads/{filename}",
            'filename': filename
        }
    except Exception as e:
        print(f"Download error: {e}")
        return {'error': str(e)}

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
        # Check cache first
        cached_results = get_cached_search(query)
        if cached_results:
            print(f"✅ CACHE HIT for: '{query}'")
            return jsonify(cached_results)
        
        print(f"🔍 API Search called for: '{query}'")
        results = fast_youtube_search(query, 10)
        
        # Cache the results
        cache_search(query, results)
        
        print(f"✅ API Search completed for: '{query}'")
        return jsonify(results)
    except Exception as e:
        print(f"❌ API Search failed for '{query}': {e}")
        return jsonify({'error': f'Search failed: {str(e)}'}), 500

@app.route('/api/suggestions', methods=['POST'])
def suggestions():
    """Get search suggestions - WORKING VERSION"""
    data = request.get_json()
    if not data:
        return jsonify({'suggestions': []})
        
    query = data.get('query', '').strip()
    if len(query) < 2:
        return jsonify({'suggestions': []})
        
    try:
        suggestions_list = get_youtube_suggestions(query)
        return jsonify({'suggestions': suggestions_list[:5]})
    except Exception as e:
        print(f"Suggestions error: {e}")
        return jsonify({'suggestions': []})

@app.route('/api/search-history')
def get_search_history():
    """Get user's search history"""
    return jsonify({'history': search_history[:10]})

# NEW: Get audio stream for native playback
@app.route('/api/stream/<video_id>')
def get_audio_stream(video_id):
    """Get direct audio stream URL for native playback"""
    try:
        stream_url = get_audio_stream_url(video_id)
        if stream_url:
            return jsonify({
                'success': True,
                'streamUrl': stream_url,
                'type': 'direct'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Could not get audio stream'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# NEW: Proxy audio stream for CORS
@app.route('/api/proxy-audio')
def proxy_audio():
    """Proxy audio stream to avoid CORS issues"""
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Range': request.headers.get('Range', ''),
        }
        
        response = requests.get(url, headers=headers, stream=True, timeout=30)
        
        return_response = app.response_class(
            response=response.iter_content(chunk_size=8192),
            status=response.status_code,
            headers=dict(response.headers),
            mimetype=response.headers.get('content-type', 'audio/mpeg')
        )
        
        return return_response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# NEW: Enhanced view count endpoint
@app.route('/api/views/<video_id>')
def get_views(video_id):
    """Get accurate view count for a video using the enhanced method"""
    try:
        from ytmusicapi import YTMusic
        yt = YTMusic()
        
        # Search for the specific video to get accurate view count
        results = yt.search(video_id, filter='videos', limit=1)
        
        if not results:
            return jsonify({'views': 0, 'error': 'Video not found'})
        
        # Get the first result (should be our video)
        item = results[0]
        views = item.get('views', '0')
        
        parsed_views = parse_view_count(views)
        
        return jsonify({
            'views': parsed_views,
            'formatted': format_views(parsed_views),
            'raw': views
        })
        
    except Exception as e:
        print(f"View count error for {video_id}: {e}")
        return jsonify({'views': 0, 'error': str(e)})

# NEW: Download queue endpoints
@app.route('/api/queue-download', methods=['POST'])
def queue_download():
    """Add download to queue"""
    data = request.get_json()
    video_id = data.get('videoId')
    title = data.get('title', 'Unknown')
    artist = data.get('artist', 'Unknown')
    
    if not video_id:
        return jsonify({'error': 'No videoId provided'}), 400
    
    # Add to queue
    download_item = {
        'video_id': video_id,
        'title': title,
        'artist': artist,
        'album': data.get('album', ''),
        'thumbnail': data.get('thumbnail', ''),
        'format': data.get('format', 'mp3'),
        'fast': data.get('fast', True),
        'queued_at': time.time(),
        'status': 'queued'
    }
    
    download_queue.append(download_item)
    
    # Start processing if not already running
    if current_downloads < MAX_CONCURRENT_DOWNLOADS:
        process_download_queue()
    
    return jsonify({
        'status': 'queued',
        'position': len(download_queue),
        'message': f'"{title}" added to download queue'
    })

@app.route('/api/download-status')
def download_status():
    """Get current download status"""
    return jsonify({
        'queue': download_queue,
        'current_downloads': current_downloads,
        'active_downloads': [item for item in download_queue if item.get('status') in ['downloading']]
    })

# Original download endpoint (kept for compatibility)
@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json()
    video_id = data.get('videoId')
    title = data.get('title', 'Unknown')
    artist = data.get('artist', 'Unknown')
    album = data.get('album', '')
    thumbnail_url = data.get('thumbnail', '')
    format = data.get('format', 'mp3')
    fast_mode = data.get('fast', False)

    if not video_id:
        return jsonify({'error': 'No videoId provided'}), 400

    result = download_internal(video_id, title, artist, album, thumbnail_url, format, fast_mode)
    
    if 'error' in result:
        return jsonify({'error': result['error']}), 500
    else:
        return jsonify(result)

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

@app.route('/api/debug-suggestions', methods=['POST'])
def debug_suggestions():
    """Debug endpoint to test suggestions"""
    data = request.get_json()
    query = data.get('query', '')
    
    print(f"🔍 DEBUG: Getting suggestions for: '{query}'")
    
    # Test the suggestions function directly
    suggestions = get_youtube_suggestions(query)
    
    print(f"🔍 DEBUG: Raw suggestions: {suggestions}")
    print(f"🔍 DEBUG: Suggestions type: {type(suggestions)}")
    print(f"🔍 DEBUG: Suggestions length: {len(suggestions)}")
    
    return jsonify({
        'query': query,
        'suggestions': suggestions,
        'suggestions_count': len(suggestions),
        'suggestions_type': str(type(suggestions))
    })

@app.route('/api/artist/<artist_id>')
def get_artist(artist_id):
    """Get artist details and songs"""
    try:
        from ytmusicapi import YTMusic
        yt = YTMusic()
        
        # Get artist information
        artist = yt.get_artist(artist_id)
        
        # Get artist's songs
        artist_songs = yt.get_artist_albums(artist_id, params="Eg-KAQwIABAAGAEgACgAMAI%3D")
        
        return jsonify({
            'artist': artist,
            'songs': artist_songs
        })
    except Exception as e:
        print(f"Artist error: {e}")
        return jsonify({'error': 'Artist not found'}), 404

@app.route('/api/library')
def get_library():
    """Get user library data"""
    try:
        if not user_authenticated:
            return jsonify({
                'library': {
                    'songs': [],
                    'artists': [],
                    'albums': [],
                    'playlists': []
                },
                'authenticated': False
            })
        
        # For now, return empty library until we implement proper library functionality
        return jsonify({
            'library': {
                'songs': [],
                'artists': [],
                'albums': [],
                'playlists': []
            },
            'authenticated': True
        })
    except Exception as e:
        print(f"Library error: {e}")
        return jsonify({
            'library': {
                'songs': [],
                'artists': [],
                'albums': [],
                'playlists': []
            },
            'authenticated': False
        })

@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    """Authenticate with YouTube Music"""
    global browser_json_content, user_authenticated
    
    data = request.get_json()
    if not data or 'browserJson' not in data:
        return jsonify({'success': False, 'error': 'No browser.json provided'})
    
    browser_json = data['browserJson']
    
    try:
        # Validate the JSON
        json.loads(browser_json)
        
        # Save the browser.json content
        browser_json_content = browser_json
        user_authenticated = True
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Authentication error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/export-data')
def export_data():
    """Export user data"""
    try:
        export_data = {
            'songs': songs_db,
            'artists': artists_db,
            'search_history': search_history
        }
        
        # Create a temporary file with the export data
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(export_data, f, indent=2)
            temp_file = f.name
        
        return send_file(temp_file, as_attachment=True, download_name='musicgrab_export.json')
    except Exception as e:
        print(f"Export error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/import-data', methods=['POST'])
def import_data():
    """Import user data"""
    global songs_db, artists_db, search_history
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'})
    
    try:
        data = json.load(file)
        
        # Update the global variables
        if 'songs' in data:
            songs_db = data['songs']
        if 'artists' in data:
            artists_db = data['artists']
        if 'search_history' in data:
            search_history = data['search_history']
        
        # Save the updated data
        save_user_data()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Import error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/direct-download/<video_id>')
def direct_download(video_id):
    """Stream download directly to user's computer - FIXED"""
    try:
        # Use settings that work with YouTube's SABR streaming
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': False,  # Set to False to see what's happening
            'no_warnings': False,
            'extract_flat': False,
            'socket_timeout': 30,
            'retries': 3,
        }
        
        print(f"🔧 Starting direct download for: {video_id}")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            title = info.get('title', 'audio')
            artist = info.get('uploader', 'Unknown Artist')
            
            # Clean filename
            sanitized_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).strip()
            sanitized_artist = "".join(c for c in artist if c.isalnum() or c in (" ", "-", "_")).strip()
            filename = f"{sanitized_artist} - {sanitized_title}.mp3"
            
            print(f"📄 Filename: {filename}")
            print(f"🎵 Title: {title}")
            print(f"🎤 Artist: {artist}")
            
            # Get direct audio URL
            audio_url = None
            
            # Method 1: Try direct URL first
            if 'url' in info:
                audio_url = info['url']
                print("✅ Using direct URL from info")
            
            # Method 2: Try formats
            if not audio_url and 'formats' in info:
                # Find audio-only formats
                audio_formats = [f for f in info['formats'] if f.get('vcodec') == 'none' and f.get('acodec') != 'none']
                print(f"🔍 Found {len(audio_formats)} audio formats")
                
                if audio_formats:
                    # Sort by quality
                    audio_formats.sort(key=lambda x: x.get('abr', 0) or 0, reverse=True)
                    
                    for i, fmt in enumerate(audio_formats[:5]):  # Try top 5
                        if fmt.get('url'):
                            audio_url = fmt['url']
                            print(f"✅ Using format {i+1}: {fmt.get('ext')} - {fmt.get('abr')}kbps")
                            break
            
            if not audio_url:
                print("❌ No audio URL found, using fallback")
                # Fallback: Use the first available format
                if 'formats' in info and info['formats']:
                    audio_url = info['formats'][0].get('url')
                    print(f"🔄 Fallback to first format: {info['formats'][0].get('ext')}")
            
            if not audio_url:
                return jsonify({'error': 'Could not extract audio stream'}), 500
            
            print(f"🔗 Audio URL obtained, streaming...")
            
            # Stream directly to user's browser for download
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Referer': 'https://www.youtube.com/',
            }
            
            response = requests.get(audio_url, headers=headers, stream=True, timeout=30)
            
            # FIX: Use Response directly (it's imported at the top)
            return Response(
                response.iter_content(chunk_size=8192),
                mimetype='audio/mpeg',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"',
                    'Content-Type': 'audio/mpeg'
                }
            )
            
    except Exception as e:
        print(f"❌ Direct download error: {e}")
        return jsonify({'error': str(e)}), 500
        
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port, debug=False)




