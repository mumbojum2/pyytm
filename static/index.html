<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MusicGrab Pro - YouTube Music Downloader</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        * {
            font-family: 'Inter', sans-serif;
        }
        
        body {
            margin: 0;
            padding: 0;
            min-height: 100vh;
            overflow-x: hidden;
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }
        
        .gradient-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            z-index: -1;
        }
        
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .glass-effect {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .gradient-text {
            background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .song-card {
            transition: all 0.3s ease;
        }
        
        .song-card:hover {
            transform: translateY(-2px);
        }
        
        .loading-spinner {
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top: 3px solid #fff;
            width: 20px;
            height: 20px;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .fade-in {
            animation: fadeIn 0.3s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .progress-bar {
            height: 4px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 2px;
            overflow: hidden;
            cursor: pointer;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
            transition: width 0.1s ease;
        }
        
        .text-ellipsis {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        /* Mobile optimizations */
        @media (max-width: 768px) {
            .mobile-hidden {
                display: none;
            }
            
            .mobile-full {
                width: 100%;
            }
            
            .mobile-padding {
                padding: 1rem;
            }
            
            .mobile-text-lg {
                font-size: 1.125rem;
            }
            
            .mobile-player-open {
                padding-bottom: 120px;
            }
        }
        
        /* Player states */
        .player-loading .play-btn i {
            animation: pulse 1.5s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        /* Navigation active state */
        .nav-active {
            background: rgba(255, 255, 255, 0.2);
            box-shadow: 0 0 10px rgba(124, 58, 237, 0.5);
        }
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 6px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.3);
            border-radius: 3px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.5);
        }
    </style>
</head>
<body class="text-white">
    <!-- Gradient Overlay -->
    <div class="gradient-overlay"></div>
    
    <!-- Navigation -->
    <nav class="glass-effect p-4 sticky top-0 z-10">
        <div class="container mx-auto flex justify-between items-center">
            <div class="flex items-center space-x-2">
                <i class="fas fa-music text-xl gradient-text"></i>
                <h1 class="text-xl font-bold gradient-text mobile-hidden">MusicGrab Pro</h1>
                <h1 class="text-xl font-bold gradient-text md:hidden">MGP</h1>
            </div>
            
            <div class="flex space-x-2">
                <button id="homeBtn" class="px-3 py-2 rounded-lg nav-active transition mobile-hidden">
                    <i class="fas fa-home mr-2"></i>Home
                </button>
                <button id="homeBtnMobile" class="p-2 rounded-lg nav-active transition md:hidden">
                    <i class="fas fa-home"></i>
                </button>
                
                <button id="libraryBtn" class="px-3 py-2 rounded-lg hover:bg-white/10 transition mobile-hidden">
                    <i class="fas fa-heart mr-2"></i>Library
                </button>
                <button id="libraryBtnMobile" class="p-2 rounded-lg hover:bg-white/10 transition md:hidden">
                    <i class="fas fa-heart"></i>
                </button>
                
                <button id="playlistsBtn" class="px-3 py-2 rounded-lg hover:bg-white/10 transition mobile-hidden">
                    <i class="fas fa-list mr-2"></i>Playlists
                </button>
                <button id="playlistsBtnMobile" class="p-2 rounded-lg hover:bg-white/10 transition md:hidden">
                    <i class="fas fa-list"></i>
                </button>
                
                <button id="downloadsBtn" class="px-3 py-2 rounded-lg hover:bg-white/10 transition mobile-hidden">
                    <i class="fas fa-download mr-2"></i>Downloads
                </button>
                <button id="downloadsBtnMobile" class="p-2 rounded-lg hover:bg-white/10 transition md:hidden">
                    <i class="fas fa-download"></i>
                </button>
            </div>
            
            <div class="flex items-center space-x-2">
                <button id="authBtn" class="px-3 py-2 rounded-lg bg-white/10 hover:bg-white/20 transition mobile-hidden">
                    <i class="fas fa-user mr-2"></i>Sign In
                </button>
                <button id="authBtnMobile" class="p-2 rounded-lg bg-white/10 hover:bg-white/20 transition md:hidden">
                    <i class="fas fa-user"></i>
                </button>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="container mx-auto p-4 mobile-padding relative z-10 mobile-player-open">
        <!-- Hero Section -->
        <section id="heroSection" class="text-center mb-8 mt-4 fade-in">
            <h1 class="text-3xl md:text-5xl font-bold mb-4 gradient-text">Discover & Download Music</h1>
            <p class="text-lg md:text-xl text-gray-200 max-w-2xl mx-auto">Find your favorite songs from YouTube Music. Stream instantly or download for offline.</p>
        </section>

        <!-- Search Section -->
        <section id="searchSection" class="mb-8 fade-in">
            <div class="max-w-2xl mx-auto">
                <div class="relative">
                    <input 
                        type="text" 
                        id="searchInput" 
                        placeholder="Search for songs, artists, or albums..." 
                        class="w-full p-4 rounded-xl glass-effect text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-400 transition-all duration-300 text-lg"
                    >
                    <button id="searchBtn" class="absolute right-2 top-2 p-3 bg-purple-600 hover:bg-purple-700 rounded-lg transition">
                        <i class="fas fa-search"></i>
                    </button>
                </div>
                
                <!-- Search Suggestions -->
                <div id="suggestions" class="mt-2 hidden">
                    <div class="glass-effect rounded-xl p-2">
                        <div id="suggestionsList" class="space-y-1"></div>
                    </div>
                </div>
                
                <!-- Search History -->
                <div id="searchHistory" class="mt-4 hidden">
                    <h3 class="text-sm font-medium mb-2">Recent Searches</h3>
                    <div id="historyList" class="flex flex-wrap gap-2"></div>
                </div>
            </div>
        </section>

        <!-- Home Section -->
        <section id="homeSection" class="fade-in">
            <!-- Featured Categories -->
            <div class="mb-8">
                <h2 class="text-2xl font-bold mb-4 text-center mobile-text-lg">Featured Categories</h2>
                <div id="featuredGrid" class="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <!-- Featured items will be loaded here -->
                </div>
            </div>
            
            <!-- Recommendations -->
            <div>
                <h2 class="text-2xl font-bold mb-4 text-center mobile-text-lg">Recommended For You</h2>
                <div id="recommendationsGrid" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
                    <!-- Recommendations will be loaded here -->
                </div>
            </div>
        </section>

        <!-- Search Results Section -->
        <section id="searchResultsSection" class="hidden fade-in">
            <div class="flex justify-between items-center mb-4">
                <h2 id="resultsTitle" class="text-2xl font-bold mobile-text-lg text-ellipsis pr-2">Search Results</h2>
                <button id="backToHome" class="px-4 py-2 rounded-lg glass-effect hover:bg-white/10 transition flex-shrink-0">
                    <i class="fas fa-arrow-left mr-2 mobile-hidden"></i>
                    <span class="md:hidden">Back</span>
                    <span class="mobile-hidden">Back to Home</span>
                </button>
            </div>
            
            <!-- Tabs -->
            <div class="mb-4">
                <div class="flex space-x-4 border-b border-white/20">
                    <button id="songsTab" class="tab-button px-4 py-2 border-b-2 border-purple-500 font-medium">Songs</button>
                    <button id="artistsTab" class="tab-button px-4 py-2 text-gray-300 hover:text-white transition">Artists</button>
                    <button id="albumsTab" class="tab-button px-4 py-2 text-gray-300 hover:text-white transition">Albums</button>
                </div>
            </div>
            
            <!-- Results Content -->
            <div id="songsResults" class="space-y-3">
                <!-- Songs will be loaded here -->
            </div>
            
            <div id="artistsResults" class="hidden grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                <!-- Artists will be loaded here -->
            </div>
            
            <div id="albumsResults" class="hidden grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                <!-- Albums will be loaded here -->
            </div>
        </section>

        <!-- Library Section -->
        <section id="librarySection" class="hidden fade-in">
            <h2 class="text-2xl font-bold mb-4 text-center mobile-text-lg">Your Library</h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <!-- Downloaded Songs -->
                <div class="glass-effect rounded-xl p-4">
                    <div class="flex justify-between items-center mb-3">
                        <h3 class="text-lg font-bold">Downloaded Songs</h3>
                        <span id="songsCount" class="bg-purple-600 px-2 py-1 rounded-full text-sm">0</span>
                    </div>
                    <div id="librarySongs" class="space-y-2 max-h-80 overflow-y-auto">
                        <!-- Downloaded songs will be loaded here -->
                    </div>
                </div>
                
                <!-- Favorite Artists -->
                <div class="glass-effect rounded-xl p-4">
                    <div class="flex justify-between items-center mb-3">
                        <h3 class="text-lg font-bold">Favorite Artists</h3>
                        <span id="artistsCount" class="bg-purple-600 px-2 py-1 rounded-full text-sm">0</span>
                    </div>
                    <div id="libraryArtists" class="space-y-2 max-h-80 overflow-y-auto">
                        <!-- Favorite artists will be loaded here -->
                    </div>
                </div>
            </div>
            
            <!-- Data Management -->
            <div class="glass-effect rounded-xl p-6 max-w-2xl mx-auto">
                <h3 class="text-xl font-bold mb-4 text-center">Data Management</h3>
                <div class="flex space-x-4 justify-center">
                    <button id="exportBtn" class="px-4 py-2 bg-green-600 hover:bg-green-700 rounded-lg transition">
                        <i class="fas fa-file-export mr-2"></i>Export Data
                    </button>
                    <button id="importBtn" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition">
                        <i class="fas fa-file-import mr-2"></i>Import Data
                    </button>
                    <input type="file" id="importFile" class="hidden" accept=".json">
                </div>
            </div>
        </section>

        <!-- Playlists Section -->
        <section id="playlistsSection" class="hidden fade-in">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-2xl font-bold mobile-text-lg">Your Playlists</h2>
                <button id="createPlaylistBtn" class="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition">
                    <i class="fas fa-plus mr-2"></i>New Playlist
                </button>
            </div>
            
            <div id="playlistsList" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <!-- Playlists will be loaded here -->
            </div>
            
            <!-- Current Playlist View -->
            <div id="currentPlaylistSection" class="hidden mt-6">
                <div class="flex justify-between items-center mb-4">
                    <h3 id="currentPlaylistName" class="text-xl font-bold">Playlist Name</h3>
                    <button id="backToPlaylists" class="px-4 py-2 rounded-lg glass-effect hover:bg-white/10 transition">
                        <i class="fas fa-arrow-left mr-2"></i>Back to Playlists
                    </button>
                </div>
                <div id="currentPlaylistSongs" class="space-y-3">
                    <!-- Playlist songs will be loaded here -->
                </div>
            </div>
        </section>

        <!-- Downloads Section -->
        <section id="downloadsSection" class="hidden fade-in">
            <h2 class="text-2xl font-bold mb-4 text-center mobile-text-lg">Your Downloads</h2>
            
            <div id="downloadsList" class="space-y-3">
                <!-- Downloads will be loaded here -->
            </div>
        </section>

        <!-- Player -->
        <div id="player" class="fixed bottom-0 left-0 right-0 glass-effect p-3 hidden z-20">
            <div class="container mx-auto">
                <!-- Loading State -->
                <div id="playerLoading" class="text-center text-sm text-gray-300 mb-2 hidden">
                    <i class="fas fa-spinner fa-spin mr-2"></i>
                    <span id="loadingSongText">Loading song...</span>
                </div>
                
                <div class="flex items-center justify-between">
                    <!-- Song Info -->
                    <div class="flex items-center space-x-3 w-1/4 min-w-0">
                        <img id="playerThumbnail" src="" alt="" class="w-10 h-10 rounded-lg hidden">
                        <div class="min-w-0 flex-1">
                            <div id="playerTitle" class="font-medium text-ellipsis text-sm">Song Title</div>
                            <div id="playerArtist" class="text-xs text-gray-300 text-ellipsis">Artist Name</div>
                        </div>
                    </div>
                    
                    <!-- Controls -->
                    <div class="flex flex-col items-center w-2/4">
                        <div class="flex items-center space-x-4 mb-1">
                            <button id="prevBtn" class="text-gray-300 hover:text-white p-2">
                                <i class="fas fa-step-backward"></i>
                            </button>
                            <button id="playBtn" class="bg-white text-purple-600 rounded-full w-8 h-8 flex items-center justify-center hover:bg-gray-200 transition">
                                <i class="fas fa-play text-xs"></i>
                            </button>
                            <button id="nextBtn" class="text-gray-300 hover:text-white p-2">
                                <i class="fas fa-step-forward"></i>
                            </button>
                        </div>
                        
                        <div class="w-full flex items-center space-x-2">
                            <span id="currentTime" class="text-xs text-gray-300">0:00</span>
                            <div class="progress-bar flex-1" id="progressBar">
                                <div id="progressFill" class="progress-fill" style="width: 0%"></div>
                            </div>
                            <span id="duration" class="text-xs text-gray-300">0:00</span>
                        </div>
                    </div>
                    
                    <!-- Actions -->
                    <div class="flex items-center justify-end space-x-2 w-1/4">
                        <button id="addToPlaylistBtn" class="text-gray-300 hover:text-white p-2" title="Add to Playlist">
                            <i class="fas fa-plus"></i>
                        </button>
                        <button id="downloadCurrentBtn" class="text-gray-300 hover:text-white p-2" title="Download">
                            <i class="fas fa-download"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- Playlist Creation Modal -->
    <div id="playlistModal" class="fixed inset-0 bg-black/70 flex items-center justify-center z-30 hidden">
        <div class="glass-effect rounded-xl p-6 max-w-md w-full mx-4">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-xl font-bold">Create New Playlist</h3>
                <button id="closePlaylistModal" class="text-gray-300 hover:text-white">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            
            <div class="mb-4">
                <label class="block text-sm font-medium mb-2">Playlist Name</label>
                <input 
                    type="text" 
                    id="playlistNameInput" 
                    placeholder="My Awesome Playlist" 
                    class="w-full p-3 rounded-lg bg-white/10 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-400"
                >
            </div>
            
            <div class="flex justify-end space-x-3">
                <button id="cancelPlaylist" class="px-4 py-2 rounded-lg glass-effect hover:bg-white/10 transition">
                    Cancel
                </button>
                <button id="createPlaylist" class="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition">
                    Create
                </button>
            </div>
        </div>
    </div>

    <!-- Add to Playlist Modal -->
    <div id="addToPlaylistModal" class="fixed inset-0 bg-black/70 flex items-center justify-center z-30 hidden">
        <div class="glass-effect rounded-xl p-6 max-w-md w-full mx-4">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-xl font-bold">Add to Playlist</h3>
                <button id="closeAddToPlaylistModal" class="text-gray-300 hover:text-white">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            
            <div id="playlistsSelect" class="mb-4 max-h-60 overflow-y-auto">
                <!-- Playlists will be listed here -->
            </div>
            
            <div class="flex justify-end space-x-3">
                <button id="cancelAddToPlaylist" class="px-4 py-2 rounded-lg glass-effect hover:bg-white/10 transition">
                    Cancel
                </button>
            </div>
        </div>
    </div>

    <!-- Authentication Modal -->
    <div id="authModal" class="fixed inset-0 bg-black/70 flex items-center justify-center z-30 hidden">
        <div class="glass-effect rounded-xl p-6 max-w-md w-full mx-4">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-xl font-bold">Sign In to YouTube Music</h3>
                <button id="closeAuthModal" class="text-gray-300 hover:text-white">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            
            <p class="text-gray-300 mb-4">
                To get personalized recommendations, sign in with your YouTube Music account.
            </p>
            
            <div class="mb-4">
                <label class="block text-sm font-medium mb-2">Paste browser.json content:</label>
                <textarea 
                    id="browserJson" 
                    rows="8" 
                    class="w-full p-3 rounded-lg bg-white/10 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-400"
                    placeholder='Paste your browser.json content here...'
                ></textarea>
            </div>
            
            <div class="flex justify-end space-x-3">
                <button id="cancelAuth" class="px-4 py-2 rounded-lg glass-effect hover:bg-white/10 transition">
                    Cancel
                </button>
                <button id="submitAuth" class="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition">
                    Sign In
                </button>
            </div>
        </div>
    </div>

    <!-- Loading Overlay -->
    <div id="loadingOverlay" class="fixed inset-0 bg-black/70 flex items-center justify-center z-30 hidden">
        <div class="text-center glass-effect p-6 rounded-xl">
            <div class="loading-spinner mx-auto mb-3"></div>
            <p id="loadingText" class="text-white">Loading...</p>
        </div>
    </div>

    <script>
        // Global variables
        let currentAudio = null;
        let currentSong = null;
        let isPlaying = false;
        let currentSection = 'home';
        let searchResults = { songs: [], artists: [], albums: [] };
        let librarySongs = [];
        let libraryArtists = [];
        let searchHistory = [];
        let playlists = {};
        let currentPlaylist = null;
        let currentPlaylistSongs = [];
        let currentPlayingContext = {
            type: null,
            id: null,
            songs: [],
            currentIndex: 0
        };

        // DOM Elements
        const searchInput = document.getElementById('searchInput');
        const searchBtn = document.getElementById('searchBtn');
        const suggestions = document.getElementById('suggestions');
        const suggestionsList = document.getElementById('suggestionsList');
        const searchHistoryContainer = document.getElementById('searchHistory');
        const historyList = document.getElementById('historyList');
        
        const homeSection = document.getElementById('homeSection');
        const searchResultsSection = document.getElementById('searchResultsSection');
        const librarySection = document.getElementById('librarySection');
        const playlistsSection = document.getElementById('playlistsSection');
        const downloadsSection = document.getElementById('downloadsSection');
        const heroSection = document.getElementById('heroSection');
        const currentPlaylistSection = document.getElementById('currentPlaylistSection');
        
        // Navigation buttons
        const homeBtn = document.getElementById('homeBtn');
        const homeBtnMobile = document.getElementById('homeBtnMobile');
        const libraryBtn = document.getElementById('libraryBtn');
        const libraryBtnMobile = document.getElementById('libraryBtnMobile');
        const playlistsBtn = document.getElementById('playlistsBtn');
        const playlistsBtnMobile = document.getElementById('playlistsBtnMobile');
        const downloadsBtn = document.getElementById('downloadsBtn');
        const downloadsBtnMobile = document.getElementById('downloadsBtnMobile');
        const backToHome = document.getElementById('backToHome');
        const backToPlaylists = document.getElementById('backToPlaylists');
        
        const featuredGrid = document.getElementById('featuredGrid');
        const recommendationsGrid = document.getElementById('recommendationsGrid');
        
        const songsTab = document.getElementById('songsTab');
        const artistsTab = document.getElementById('artistsTab');
        const albumsTab = document.getElementById('albumsTab');
        
        const songsResults = document.getElementById('songsResults');
        const artistsResults = document.getElementById('artistsResults');
        const albumsResults = document.getElementById('albumsResults');
        const resultsTitle = document.getElementById('resultsTitle');
        
        const authBtn = document.getElementById('authBtn');
        const authBtnMobile = document.getElementById('authBtnMobile');
        const authModal = document.getElementById('authModal');
        const closeAuthModal = document.getElementById('closeAuthModal');
        const cancelAuth = document.getElementById('cancelAuth');
        const submitAuth = document.getElementById('submitAuth');
        const browserJson = document.getElementById('browserJson');
        
        const librarySongsContainer = document.getElementById('librarySongs');
        const libraryArtistsContainer = document.getElementById('libraryArtists');
        const songsCount = document.getElementById('songsCount');
        const artistsCount = document.getElementById('artistsCount');
        
        const downloadsList = document.getElementById('downloadsList');
        
        const playlistsList = document.getElementById('playlistsList');
        const createPlaylistBtn = document.getElementById('createPlaylistBtn');
        const currentPlaylistName = document.getElementById('currentPlaylistName');
        const currentPlaylistSongsContainer = document.getElementById('currentPlaylistSongs');
        
        // Player elements
        const player = document.getElementById('player');
        const playerLoading = document.getElementById('playerLoading');
        const loadingSongText = document.getElementById('loadingSongText');
        const playerThumbnail = document.getElementById('playerThumbnail');
        const playerTitle = document.getElementById('playerTitle');
        const playerArtist = document.getElementById('playerArtist');
        const playBtn = document.getElementById('playBtn');
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const downloadCurrentBtn = document.getElementById('downloadCurrentBtn');
        const addToPlaylistBtn = document.getElementById('addToPlaylistBtn');
        const currentTime = document.getElementById('currentTime');
        const duration = document.getElementById('duration');
        const progressFill = document.getElementById('progressFill');
        const progressBar = document.getElementById('progressBar');
        
        // Modal elements
        const playlistModal = document.getElementById('playlistModal');
        const closePlaylistModal = document.getElementById('closePlaylistModal');
        const cancelPlaylist = document.getElementById('cancelPlaylist');
        const createPlaylist = document.getElementById('createPlaylist');
        const playlistNameInput = document.getElementById('playlistNameInput');
        
        const addToPlaylistModal = document.getElementById('addToPlaylistModal');
        const closeAddToPlaylistModal = document.getElementById('closeAddToPlaylistModal');
        const cancelAddToPlaylist = document.getElementById('cancelAddToPlaylist');
        const playlistsSelect = document.getElementById('playlistsSelect');
        
        const loadingOverlay = document.getElementById('loadingOverlay');
        const loadingText = document.getElementById('loadingText');

        // Export/Import
        const exportBtn = document.getElementById('exportBtn');
        const importBtn = document.getElementById('importBtn');
        const importFile = document.getElementById('importFile');

        // Event Listeners
        document.addEventListener('DOMContentLoaded', () => {
            loadHomeData();
            loadSearchHistory();
            loadPlaylists();
            
            // Navigation
            homeBtn.addEventListener('click', () => showSection('home'));
            homeBtnMobile.addEventListener('click', () => showSection('home'));
            libraryBtn.addEventListener('click', () => showSection('library'));
            libraryBtnMobile.addEventListener('click', () => showSection('library'));
            playlistsBtn.addEventListener('click', () => showSection('playlists'));
            playlistsBtnMobile.addEventListener('click', () => showSection('playlists'));
            downloadsBtn.addEventListener('click', () => showSection('downloads'));
            downloadsBtnMobile.addEventListener('click', () => showSection('downloads'));
            backToHome.addEventListener('click', () => showSection('home'));
            backToPlaylists.addEventListener('click', () => showPlaylistsList());
            
            // Search
            searchInput.addEventListener('input', handleSearchInput);
            searchBtn.addEventListener('click', performSearch);
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') performSearch();
            });
            
            // Tabs
            songsTab.addEventListener('click', () => showResultsTab('songs'));
            artistsTab.addEventListener('click', () => showResultsTab('artists'));
            albumsTab.addEventListener('click', () => showResultsTab('albums'));
            
            // Authentication
            authBtn.addEventListener('click', () => authModal.classList.remove('hidden'));
            authBtnMobile.addEventListener('click', () => authModal.classList.remove('hidden'));
            closeAuthModal.addEventListener('click', () => authModal.classList.add('hidden'));
            cancelAuth.addEventListener('click', () => authModal.classList.add('hidden'));
            submitAuth.addEventListener('click', submitAuthentication);
            
            // Playlists
            createPlaylistBtn.addEventListener('click', () => playlistModal.classList.remove('hidden'));
            closePlaylistModal.addEventListener('click', () => playlistModal.classList.add('hidden'));
            cancelPlaylist.addEventListener('click', () => playlistModal.classList.add('hidden'));
            createPlaylist.addEventListener('click', createNewPlaylist);
            
            closeAddToPlaylistModal.addEventListener('click', () => addToPlaylistModal.classList.add('hidden'));
            cancelAddToPlaylist.addEventListener('click', () => addToPlaylistModal.classList.add('hidden'));
            addToPlaylistBtn.addEventListener('click', showAddToPlaylistModal);
            
            // Player
            playBtn.addEventListener('click', togglePlay);
            prevBtn.addEventListener('click', playPreviousSong);
            nextBtn.addEventListener('click', playNextSong);
            downloadCurrentBtn.addEventListener('click', downloadCurrentSong);
            
            // Progress bar seeking
            progressBar.addEventListener('click', seekAudio);
            
            // Export/Import
            exportBtn.addEventListener('click', exportData);
            importBtn.addEventListener('click', () => importFile.click());
            importFile.addEventListener('change', importData);
            
            // Close modals when clicking outside
            document.addEventListener('click', (e) => {
                if (!searchInput.contains(e.target) && !suggestions.contains(e.target)) {
                    suggestions.classList.add('hidden');
                }
                
                if (e.target === playlistModal) {
                    playlistModal.classList.add('hidden');
                }
                
                if (e.target === addToPlaylistModal) {
                    addToPlaylistModal.classList.add('hidden');
                }
                
                if (e.target === authModal) {
                    authModal.classList.add('hidden');
                }
            });
        });

        // API Functions
        async function apiCall(endpoint, options = {}) {
            try {
                const response = await fetch(endpoint, {
                    headers: {
                        'Content-Type': 'application/json',
                        ...options.headers
                    },
                    ...options
                });
                
                if (!response.ok) {
                    throw new Error(`API error: ${response.status}`);
                }
                
                return await response.json();
            } catch (error) {
                console.error('API call failed:', error);
                showNotification('An error occurred. Please try again.', 'error');
                throw error;
            }
        }

        // UI Functions
        function showSection(section) {
            // Hide all sections
            homeSection.classList.add('hidden');
            searchResultsSection.classList.add('hidden');
            librarySection.classList.add('hidden');
            playlistsSection.classList.add('hidden');
            downloadsSection.classList.add('hidden');
            heroSection.classList.add('hidden');
            currentPlaylistSection.classList.add('hidden');
            
            // Remove active state from all nav buttons
            document.querySelectorAll('nav button').forEach(btn => {
                btn.classList.remove('nav-active');
            });
            
            // Show selected section
            if (section === 'home') {
                homeSection.classList.remove('hidden');
                heroSection.classList.remove('hidden');
                homeBtn.classList.add('nav-active');
                homeBtnMobile.classList.add('nav-active');
                currentSection = 'home';
            } else if (section === 'search') {
                searchResultsSection.classList.remove('hidden');
                currentSection = 'search';
            } else if (section === 'library') {
                librarySection.classList.remove('hidden');
                libraryBtn.classList.add('nav-active');
                libraryBtnMobile.classList.add('nav-active');
                loadLibraryData();
                currentSection = 'library';
            } else if (section === 'playlists') {
                playlistsSection.classList.remove('hidden');
                playlistsBtn.classList.add('nav-active');
                playlistsBtnMobile.classList.add('nav-active');
                loadPlaylists();
                currentSection = 'playlists';
            } else if (section === 'downloads') {
                downloadsSection.classList.remove('hidden');
                downloadsBtn.classList.add('nav-active');
                downloadsBtnMobile.classList.add('nav-active');
                loadDownloadsData();
                currentSection = 'downloads';
            }
        }

        function showPlaylistsList() {
            currentPlaylistSection.classList.add('hidden');
            playlistsList.classList.remove('hidden');
            createPlaylistBtn.classList.remove('hidden');
        }

        function showCurrentPlaylist(playlist) {
            currentPlaylist = playlist;
            currentPlaylistName.textContent = playlist.name;
            currentPlaylistSongs = playlist.songs || [];
            
            playlistsList.classList.add('hidden');
            createPlaylistBtn.classList.add('hidden');
            currentPlaylistSection.classList.remove('hidden');
            
            renderPlaylistSongs();
        }

        function showResultsTab(tab) {
            // Update tab buttons
            document.querySelectorAll('.tab-button').forEach(btn => {
                btn.classList.remove('border-purple-500', 'font-medium');
                btn.classList.add('text-gray-300');
            });
            
            // Hide all result sections
            songsResults.classList.add('hidden');
            artistsResults.classList.add('hidden');
            albumsResults.classList.add('hidden');
            
            // Show selected tab
            if (tab === 'songs') {
                songsTab.classList.add('border-purple-500', 'font-medium');
                songsTab.classList.remove('text-gray-300');
                songsResults.classList.remove('hidden');
            } else if (tab === 'artists') {
                artistsTab.classList.add('border-purple-500', 'font-medium');
                artistsTab.classList.remove('text-gray-300');
                artistsResults.classList.remove('hidden');
            } else if (tab === 'albums') {
                albumsTab.classList.add('border-purple-500', 'font-medium');
                albumsTab.classList.remove('text-gray-300');
                albumsResults.classList.remove('hidden');
            }
        }

        function showLoading(message = 'Loading...') {
            loadingText.textContent = message;
            loadingOverlay.classList.remove('hidden');
        }

        function hideLoading() {
            loadingOverlay.classList.add('hidden');
        }

        function showPlayerLoading(message = 'Loading song...') {
            loadingSongText.textContent = message;
            playerLoading.classList.remove('hidden');
            player.classList.add('player-loading');
        }

        function hidePlayerLoading() {
            playerLoading.classList.add('hidden');
            player.classList.remove('player-loading');
        }

        function showNotification(message, type = 'info') {
            // Create notification element
            const notification = document.createElement('div');
            notification.className = `fixed top-4 right-4 p-4 rounded-lg z-40 fade-in glass-effect ${
                type === 'error' ? 'border-l-4 border-red-500' : 
                type === 'success' ? 'border-l-4 border-green-500' : 'border-l-4 border-blue-500'
            }`;
            notification.innerHTML = `
                <div class="flex items-center">
                    <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : type === 'success' ? 'check-circle' : 'info-circle'} mr-2 ${
                        type === 'error' ? 'text-red-400' : 
                        type === 'success' ? 'text-green-400' : 'text-blue-400'
                    }"></i>
                    <span>${message}</span>
                </div>
            `;
            
            document.body.appendChild(notification);
            
            // Remove after 3 seconds
            setTimeout(() => {
                notification.classList.add('opacity-0', 'transition-opacity', 'duration-300');
                setTimeout(() => {
                    if (document.body.contains(notification)) {
                        document.body.removeChild(notification);
                    }
                }, 300);
            }, 3000);
        }

        // Data Loading Functions
        async function loadHomeData() {
            try {
                showLoading('Loading recommendations...');
                const data = await apiCall('/api/home');
                
                // Render featured items
                featuredGrid.innerHTML = '';
                if (data.featured && data.featured.length > 0) {
                    data.featured.forEach(item => {
                        const featuredItem = document.createElement('div');
                        featuredItem.className = 'glass-effect rounded-xl p-4 song-card cursor-pointer text-center';
                        featuredItem.innerHTML = `
                            <div class="flex items-center justify-center w-12 h-12 rounded-lg ${item.color} mb-3 mx-auto">
                                <i class="${item.icon} text-white text-xl"></i>
                            </div>
                            <h3 class="font-bold text-sm">${item.title}</h3>
                            <p class="text-gray-300 text-xs">${item.subtitle}</p>
                        `;
                        featuredItem.addEventListener('click', () => {
                            searchInput.value = item.title;
                            performSearch();
                        });
                        featuredGrid.appendChild(featuredItem);
                    });
                }
                
                // Render recommendations
                recommendationsGrid.innerHTML = '';
                if (data.recommendations && data.recommendations.length > 0) {
                    data.recommendations.forEach(song => {
                        const songCard = createSongCard(song);
                        recommendationsGrid.appendChild(songCard);
                    });
                }
                
            } catch (error) {
                console.error('Failed to load home data:', error);
            } finally {
                hideLoading();
            }
        }

        async function loadSearchHistory() {
            try {
                const data = await apiCall('/api/search-history');
                if (data.history && data.history.length > 0) {
                    searchHistory = data.history;
                    searchHistoryContainer.classList.remove('hidden');
                    historyList.innerHTML = '';
                    
                    data.history.forEach(term => {
                        const historyItem = document.createElement('button');
                        historyItem.className = 'px-3 py-1 rounded-full glass-effect text-sm hover:bg-white/10 transition';
                        historyItem.textContent = term;
                        historyItem.addEventListener('click', () => {
                            searchInput.value = term;
                            performSearch();
                        });
                        historyList.appendChild(historyItem);
                    });
                } else {
                    searchHistoryContainer.classList.add('hidden');
                }
            } catch (error) {
                console.error('Failed to load search history:', error);
                searchHistoryContainer.classList.add('hidden');
            }
        }

        async function loadPlaylists() {
            try {
                const data = await apiCall('/api/playlists');
                playlists = data.playlists || {};
                renderPlaylists();
            } catch (error) {
                console.error('Failed to load playlists:', error);
                playlists = {};
            }
        }

        function renderPlaylists() {
            playlistsList.innerHTML = '';
            
            if (Object.keys(playlists).length === 0) {
                playlistsList.innerHTML = `
                    <div class="col-span-full text-center py-8">
                        <i class="fas fa-list text-4xl text-gray-400 mb-3"></i>
                        <p class="text-gray-400">No playlists yet</p>
                        <p class="text-gray-500 text-sm">Create your first playlist to get started</p>
                    </div>
                `;
                return;
            }
            
            Object.values(playlists).forEach(playlist => {
                const playlistElement = document.createElement('div');
                playlistElement.className = 'glass-effect rounded-xl p-4 song-card cursor-pointer';
                playlistElement.innerHTML = `
                    <div class="flex items-center space-x-3">
                        <div class="w-12 h-12 rounded-lg bg-purple-600 flex items-center justify-center">
                            <i class="fas fa-list text-white"></i>
                        </div>
                        <div class="flex-1 min-w-0">
                            <h3 class="font-bold text-ellipsis">${playlist.name}</h3>
                            <p class="text-gray-300 text-sm">${playlist.songs.length} songs</p>
                        </div>
                    </div>
                `;
                playlistElement.addEventListener('click', () => showCurrentPlaylist(playlist));
                playlistsList.appendChild(playlistElement);
            });
        }

        function renderPlaylistSongs() {
            currentPlaylistSongsContainer.innerHTML = '';
            
            if (currentPlaylistSongs.length === 0) {
                currentPlaylistSongsContainer.innerHTML = `
                    <div class="text-center py-8">
                        <i class="fas fa-music text-4xl text-gray-400 mb-3"></i>
                        <p class="text-gray-400">No songs in this playlist</p>
                        <p class="text-gray-500 text-sm">Add songs from search results</p>
                    </div>
                `;
                return;
            }
            
            currentPlaylistSongs.forEach(song => {
                const songElement = createSongResultElement(song);
                currentPlaylistSongsContainer.appendChild(songElement);
            });
        }

        async function loadLibraryData() {
            try {
                const data = await apiCall('/api/library');
                
                // Load songs
                librarySongs = data.library?.songs || [];
                
                // Load artists
                libraryArtists = Object.entries(data.library?.artists || {})
                    .sort((a, b) => b[1] - a[1])
                    .slice(0, 10);
                
                // Update counts
                songsCount.textContent = librarySongs.length;
                artistsCount.textContent = libraryArtists.length;
                
                // Render songs
                librarySongsContainer.innerHTML = '';
                if (librarySongs.length > 0) {
                    librarySongs.forEach(song => {
                        const songElement = document.createElement('div');
                        songElement.className = 'flex items-center justify-between p-3 rounded-lg hover:bg-white/5 transition';
                        songElement.innerHTML = `
                            <div class="flex items-center space-x-3">
                                ${song.thumbnail ? 
                                    `<img src="${song.thumbnail}" alt="${song.title}" class="w-10 h-10 rounded">` :
                                    `<div class="w-10 h-10 rounded bg-purple-600 flex items-center justify-center">
                                        <i class="fas fa-music"></i>
                                    </div>`
                                }
                                <div class="min-w-0 flex-1">
                                    <div class="font-medium text-ellipsis">${song.title}</div>
                                    <div class="text-sm text-gray-300 text-ellipsis">${song.artist}</div>
                                </div>
                            </div>
                            <button class="play-song-btn px-3 py-1 rounded-lg bg-purple-600 hover:bg-purple-700 transition" data-id="${song.id}">
                                <i class="fas fa-play"></i>
                            </button>
                        `;
                        librarySongsContainer.appendChild(songElement);
                    });
                    
                    // Add event listeners to play buttons
                    document.querySelectorAll('.play-song-btn').forEach(btn => {
                        btn.addEventListener('click', (e) => {
                            e.stopPropagation();
                            const songId = btn.getAttribute('data-id');
                            const song = librarySongs.find(s => s.id === songId);
                            if (song) playSong(song);
                        });
                    });
                } else {
                    librarySongsContainer.innerHTML = '<p class="text-gray-400 text-center py-4">No songs in your library yet</p>';
                }
                
                // Render artists
                libraryArtistsContainer.innerHTML = '';
                if (libraryArtists.length > 0) {
                    libraryArtists.forEach(([artist, count]) => {
                        const artistElement = document.createElement('div');
                        artistElement.className = 'flex items-center justify-between p-3 rounded-lg hover:bg-white/5 transition';
                        artistElement.innerHTML = `
                            <div class="flex items-center space-x-3">
                                <div class="w-10 h-10 rounded-full bg-purple-600 flex items-center justify-center">
                                    <i class="fas fa-user"></i>
                                </div>
                                <div class="min-w-0 flex-1">
                                    <div class="font-medium text-ellipsis">${artist}</div>
                                    <div class="text-sm text-gray-300">${count} song${count !== 1 ? 's' : ''}</div>
                                </div>
                            </div>
                            <button class="search-artist-btn px-3 py-1 rounded-lg glass-effect hover:bg-white/10 transition" data-artist="${artist}">
                                <i class="fas fa-search"></i>
                            </button>
                        `;
                        libraryArtistsContainer.appendChild(artistElement);
                    });
                    
                    // Add event listeners to search buttons
                    document.querySelectorAll('.search-artist-btn').forEach(btn => {
                        btn.addEventListener('click', (e) => {
                            e.stopPropagation();
                            const artist = btn.getAttribute('data-artist');
                            searchInput.value = artist;
                            performSearch();
                        });
                    });
                } else {
                    libraryArtistsContainer.innerHTML = '<p class="text-gray-400 text-center py-4">No favorite artists yet</p>';
                }
                
            } catch (error) {
                console.error('Failed to load library data:', error);
                showNotification('Failed to load library', 'error');
            }
        }

        async function loadDownloadsData() {
            try {
                const data = await apiCall('/api/songs');
                downloadsList.innerHTML = '';
                
                if (data.songs && data.songs.length > 0) {
                    data.songs.forEach(song => {
                        const downloadItem = document.createElement('div');
                        downloadItem.className = 'glass-effect rounded-xl p-4 flex items-center justify-between';
                        downloadItem.innerHTML = `
                            <div class="flex items-center space-x-4">
                                ${song.thumbnail ? 
                                    `<img src="${song.thumbnail}" alt="${song.title}" class="w-12 h-12 rounded-lg">` :
                                    `<div class="w-12 h-12 rounded-lg bg-purple-600 flex items-center justify-center">
                                        <i class="fas fa-music"></i>
                                    </div>`
                                }
                                <div class="min-w-0 flex-1">
                                    <div class="font-bold text-ellipsis">${song.title}</div>
                                    <div class="text-gray-300 text-ellipsis">${song.artist}</div>
                                    <div class="text-sm text-gray-400">Downloaded: ${song.downloaded_at || 'Unknown'}</div>
                                </div>
                            </div>
                            <div class="flex space-x-2">
                                <button class="play-download-btn px-3 py-2 rounded-lg bg-purple-600 hover:bg-purple-700 transition" data-id="${song.id}">
                                    <i class="fas fa-play"></i>
                                </button>
                                <button class="download-again-btn px-3 py-2 rounded-lg bg-green-600 hover:bg-green-700 transition" data-id="${song.id}" data-title="${song.title}" data-artist="${song.artist}">
                                    <i class="fas fa-download"></i>
                                </button>
                            </div>
                        `;
                        downloadsList.appendChild(downloadItem);
                    });
                    
                    // Add event listeners to play buttons
                    document.querySelectorAll('.play-download-btn').forEach(btn => {
                        btn.addEventListener('click', (e) => {
                            e.stopPropagation();
                            const songId = btn.getAttribute('data-id');
                            const song = data.songs.find(s => s.id === songId);
                            if (song) playSong(song);
                        });
                    });
                    
                    // Add event listeners to download-again buttons
                    document.querySelectorAll('.download-again-btn').forEach(btn => {
                        btn.addEventListener('click', (e) => {
                            e.stopPropagation();
                            const song = {
                                id: btn.getAttribute('data-id'),
                                title: btn.getAttribute('data-title'),
                                artist: btn.getAttribute('data-artist')
                            };
                            directDownload(song);
                        });
                    });
                } else {
                    downloadsList.innerHTML = '<p class="text-gray-400 text-center py-8">No downloads yet</p>';
                }
            } catch (error) {
                console.error('Failed to load downloads:', error);
                showNotification('Failed to load downloads', 'error');
            }
        }

        // Search Functions
        async function handleSearchInput() {
            const query = searchInput.value.trim();
            
            if (query.length < 2) {
                suggestions.classList.add('hidden');
                return;
            }
            
            try {
                const data = await apiCall('/api/suggestions', {
                    method: 'POST',
                    body: JSON.stringify({ query })
                });
                
                if (data.suggestions && data.suggestions.length > 0) {
                    suggestionsList.innerHTML = '';
                    data.suggestions.forEach(suggestion => {
                        const suggestionItem = document.createElement('div');
                        suggestionItem.className = 'p-2 rounded-lg hover:bg-white/10 cursor-pointer transition';
                        suggestionItem.textContent = suggestion;
                        suggestionItem.addEventListener('click', () => {
                            searchInput.value = suggestion;
                            suggestions.classList.add('hidden');
                            performSearch();
                        });
                        suggestionsList.appendChild(suggestionItem);
                    });
                    suggestions.classList.remove('hidden');
                } else {
                    suggestions.classList.add('hidden');
                }
            } catch (error) {
                suggestions.classList.add('hidden');
            }
        }

        async function performSearch() {
            const query = searchInput.value.trim();
            
            if (!query) {
                showNotification('Please enter a search term', 'error');
                return;
            }
            
            try {
                showLoading(`Searching for "${query}"...`);
                resultsTitle.textContent = `Results for "${query}"`;
                
                const data = await apiCall('/api/search', {
                    method: 'POST',
                    body: JSON.stringify({ query })
                });
                
                searchResults = data;
                renderSearchResults();
                showSection('search');
                showResultsTab('songs');
                
                // Set current playing context to search results
                currentPlayingContext = {
                    type: 'search',
                    id: query,
                    songs: data.songs || [],
                    currentIndex: 0
                };
                
                // Add to search history (frontend only)
                if (!searchHistory.includes(query)) {
                    searchHistory.unshift(query);
                    if (searchHistory.length > 10) searchHistory.pop();
                    loadSearchHistory();
                }
                
            } catch (error) {
                console.error('Search failed:', error);
            } finally {
                hideLoading();
            }
        }

        function renderSearchResults() {
            // Render songs
            songsResults.innerHTML = '';
            if (searchResults.songs && searchResults.songs.length > 0) {
                searchResults.songs.forEach(song => {
                    const songElement = createSongResultElement(song);
                    songsResults.appendChild(songElement);
                });
            } else {
                songsResults.innerHTML = '<p class="text-gray-400 text-center py-8">No songs found</p>';
            }
            
            // Render artists
            artistsResults.innerHTML = '';
            if (searchResults.artists && searchResults.artists.length > 0) {
                searchResults.artists.forEach(artist => {
                    const artistElement = document.createElement('div');
                    artistElement.className = 'glass-effect rounded-xl p-4 song-card text-center';
                    artistElement.innerHTML = `
                        ${artist.thumbnail ? 
                            `<img src="${artist.thumbnail}" alt="${artist.name}" class="w-24 h-24 rounded-full mx-auto mb-3">` :
                            `<div class="w-24 h-24 rounded-full bg-purple-600 flex items-center justify-center mx-auto mb-3">
                                <i class="fas fa-user text-2xl"></i>
                            </div>`
                        }
                        <h3 class="font-bold text-ellipsis">${artist.name}</h3>
                        <p class="text-gray-300 text-sm">Artist</p>
                        <button class="mt-3 px-4 py-2 rounded-lg bg-purple-600 hover:bg-purple-700 transition w-full view-artist-btn" data-id="${artist.id}">
                            View Artist
                        </button>
                    `;
                    artistsResults.appendChild(artistElement);
                });
            } else {
                artistsResults.innerHTML = '<p class="text-gray-400 text-center py-8">No artists found</p>';
            }
            
            // Render albums
            albumsResults.innerHTML = '';
            if (searchResults.albums && searchResults.albums.length > 0) {
                searchResults.albums.forEach(album => {
                    const albumElement = document.createElement('div');
                    albumElement.className = 'glass-effect rounded-xl p-4 song-card';
                    albumElement.innerHTML = `
                        ${album.thumbnail ? 
                            `<img src="${album.thumbnail}" alt="${album.title}" class="w-full aspect-square rounded-lg mb-3">` :
                            `<div class="w-full aspect-square rounded-lg bg-purple-600 flex items-center justify-center mb-3">
                                <i class="fas fa-compact-disc text-3xl"></i>
                            </div>`
                        }
                        <h3 class="font-bold text-ellipsis">${album.title}</h3>
                        <p class="text-gray-300 text-sm text-ellipsis">${album.artist}</p>
                        <p class="text-gray-400 text-xs">${album.year || ''}</p>
                        <button class="mt-3 px-4 py-2 rounded-lg bg-purple-600 hover:bg-purple-700 transition w-full view-album-btn" data-id="${album.id}">
                            View Album
                        </button>
                    `;
                    albumsResults.appendChild(albumElement);
                });
            } else {
                albumsResults.innerHTML = '<p class="text-gray-400 text-center py-8">No albums found</p>';
            }
        }

        function createSongResultElement(song) {
            const element = document.createElement('div');
            element.className = 'glass-effect rounded-xl p-4 flex items-center justify-between song-card';
            element.innerHTML = `
                <div class="flex items-center space-x-3 flex-1 min-w-0">
                    ${song.thumbnail ? 
                        `<img src="${song.thumbnail}" alt="${song.title}" class="w-12 h-12 rounded-lg flex-shrink-0">` :
                        `<div class="w-12 h-12 rounded-lg bg-purple-600 flex items-center justify-center flex-shrink-0">
                            <i class="fas fa-music"></i>
                        </div>`
                    }
                    <div class="flex-1 min-w-0">
                        <div class="font-bold text-sm text-ellipsis flex items-center">
                            ${song.title}
                            ${song.is_explicit ? '<span class="ml-1 px-1 bg-gray-700 text-xs rounded text-gray-300">E</span>' : ''}
                        </div>
                        <div class="text-gray-300 text-xs text-ellipsis">${song.artist}</div>
                        <div class="text-gray-400 text-xs flex items-center space-x-2 mt-1">
                            <span>${song.duration || '0:00'}</span>
                            <span>•</span>
                            <span>${song.views || 'No views'}</span>
                        </div>
                    </div>
                </div>
                <div class="flex space-x-1 flex-shrink-0">
                    <button class="play-btn p-2 rounded-lg bg-purple-600 hover:bg-purple-700 transition" data-id="${song.id}">
                        <i class="fas fa-play text-xs"></i>
                    </button>
                    <button class="download-btn p-2 rounded-lg bg-green-600 hover:bg-green-700 transition" data-id="${song.id}">
                        <i class="fas fa-download text-xs"></i>
                    </button>
                    <button class="add-to-playlist-btn p-2 rounded-lg bg-blue-600 hover:bg-blue-700 transition" data-id="${song.id}">
                        <i class="fas fa-plus text-xs"></i>
                    </button>
                </div>
            `;
            
            // Add event listeners
            element.querySelector('.play-btn').addEventListener('click', (e) => {
                e.stopPropagation();
                playSong(song);
            });
            
            element.querySelector('.download-btn').addEventListener('click', (e) => {
                e.stopPropagation();
                directDownload(song);
            });
            
            element.querySelector('.add-to-playlist-btn').addEventListener('click', (e) => {
                e.stopPropagation();
                currentSong = song;
                showAddToPlaylistModal();
            });
            
            // Click anywhere on the card to play
            element.addEventListener('click', () => {
                playSong(song);
            });
            
            return element;
        }

        function createSongCard(song) {
            const card = document.createElement('div');
            card.className = 'glass-effect rounded-xl p-3 song-card cursor-pointer';
            card.innerHTML = `
                ${song.thumbnail ? 
                    `<img src="${song.thumbnail}" alt="${song.title}" class="w-full aspect-square rounded-lg mb-2 object-cover">` :
                    `<div class="w-full aspect-square rounded-lg bg-purple-600 flex items-center justify-center mb-2">
                        <i class="fas fa-music text-xl"></i>
                    </div>`
                }
                <h3 class="font-bold text-sm text-ellipsis">${song.title}</h3>
                <p class="text-gray-300 text-xs text-ellipsis">${song.artist}</p>
                <div class="flex justify-between items-center mt-2">
                    <span class="text-xs text-gray-400">${song.views || 'Popular'}</span>
                    <button class="play-card-btn p-1 rounded-full bg-purple-600 hover:bg-purple-700 transition">
                        <i class="fas fa-play text-xs"></i>
                    </button>
                </div>
            `;
            
            card.addEventListener('click', (e) => {
                if (!e.target.closest('.play-card-btn')) {
                    playSong(song);
                }
            });
            
            card.querySelector('.play-card-btn').addEventListener('click', (e) => {
                e.stopPropagation();
                playSong(song);
            });
            
            return card;
        }

        // Player Functions
        async function playSong(song) {
            try {
                showPlayerLoading(`Loading ${song.title}...`);
                
                // Stop current audio if playing
                if (currentAudio) {
                    currentAudio.pause();
                    currentAudio = null;
                }
                
                currentSong = song;
                
                // Update player UI immediately
                playerTitle.textContent = song.title;
                playerArtist.textContent = song.artist;
                
                if (song.thumbnail) {
                    playerThumbnail.src = song.thumbnail;
                    playerThumbnail.classList.remove('hidden');
                } else {
                    playerThumbnail.classList.add('hidden');
                }
                
                // Show player
                player.classList.remove('hidden');
                
                // Try to get direct stream URL
                const streamData = await apiCall(`/api/stream/${song.id}`);
                
                if (streamData.success) {
                    currentAudio = new Audio(streamData.streamUrl);
                } else {
                    // Fallback: Use proxy
                    const proxyUrl = `/api/proxy-audio?url=${encodeURIComponent(`https://www.youtube.com/watch?v=${song.id}`)}`;
                    currentAudio = new Audio(proxyUrl);
                }
                
                // Set up audio event listeners
                currentAudio.addEventListener('loadedmetadata', () => {
                    duration.textContent = formatTime(currentAudio.duration);
                    hidePlayerLoading();
                });
                
                currentAudio.addEventListener('timeupdate', () => {
                    currentTime.textContent = formatTime(currentAudio.currentTime);
                    const progress = (currentAudio.currentTime / currentAudio.duration) * 100;
                    progressFill.style.width = `${progress}%`;
                });
                
                currentAudio.addEventListener('ended', () => {
                    isPlaying = false;
                    playBtn.innerHTML = '<i class="fas fa-play text-xs"></i>';
                    playNextSong(); // Auto-play next song
                });
                
                currentAudio.addEventListener('error', () => {
                    hidePlayerLoading();
                    showNotification('Failed to play audio', 'error');
                });
                
                // Play audio
                await currentAudio.play();
                isPlaying = true;
                playBtn.innerHTML = '<i class="fas fa-pause text-xs"></i>';
                
            } catch (error) {
                console.error('Playback failed:', error);
                hidePlayerLoading();
                showNotification('Playback failed', 'error');
            }
        }

        function togglePlay() {
            if (!currentAudio) return;
            
            if (isPlaying) {
                currentAudio.pause();
                isPlaying = false;
                playBtn.innerHTML = '<i class="fas fa-play text-xs"></i>';
            } else {
                currentAudio.play();
                isPlaying = true;
                playBtn.innerHTML = '<i class="fas fa-pause text-xs"></i>';
            }
        }

        async function playPreviousSong() {
            if (!currentSong || !currentPlayingContext.songs.length) {
                showNotification('No previous song', 'info');
                return;
            }
            
            try {
                const data = await apiCall(`/api/previous-song/${currentSong.id}`);
                if (data.previous_song) {
                    playSong(data.previous_song);
                } else {
                    showNotification('No previous song', 'info');
                }
            } catch (error) {
                console.error('Failed to get previous song:', error);
                showNotification('No previous song', 'info');
            }
        }

        async function playNextSong() {
            if (!currentSong || !currentPlayingContext.songs.length) {
                showNotification('No next song', 'info');
                return;
            }
            
            try {
                const data = await apiCall(`/api/next-song/${currentSong.id}`);
                if (data.next_song) {
                    playSong(data.next_song);
                } else {
                    showNotification('No next song', 'info');
                }
            } catch (error) {
                console.error('Failed to get next song:', error);
                showNotification('No next song', 'info');
            }
        }

        function seekAudio(e) {
            if (!currentAudio) return;
            
            const progressBar = e.currentTarget;
            const clickPosition = e.offsetX;
            const progressBarWidth = progressBar.clientWidth;
            const seekTime = (clickPosition / progressBarWidth) * currentAudio.duration;
            
            currentAudio.currentTime = seekTime;
        }

        function downloadCurrentSong() {
            if (currentSong) {
                directDownload(currentSong);
            }
        }

        function formatTime(seconds) {
            if (isNaN(seconds)) return '0:00';
            
            const mins = Math.floor(seconds / 60);
            const secs = Math.floor(seconds % 60);
            return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
        }

        // Download Functions
        function directDownload(song) {
            // This will download directly to your PC
            const downloadUrl = `/api/direct-download/${song.id}`;
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.download = `${song.artist} - ${song.title}.mp3`;
            link.style.display = 'none';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            showNotification(`Downloading "${song.title}" to your computer...`, 'success');
        }

        // Playlist Functions
        async function createNewPlaylist() {
            const name = playlistNameInput.value.trim();
            
            if (!name) {
                showNotification('Please enter a playlist name', 'error');
                return;
            }
            
            try {
                const data = await apiCall('/api/playlists', {
                    method: 'POST',
                    body: JSON.stringify({ name })
                });
                
                if (data.success) {
                    playlistModal.classList.add('hidden');
                    playlistNameInput.value = '';
                    showNotification('Playlist created successfully!', 'success');
                    loadPlaylists();
                }
            } catch (error) {
                console.error('Failed to create playlist:', error);
            }
        }

        async function addSongToPlaylist(playlistId, song) {
            try {
                const data = await apiCall(`/api/playlists/${playlistId}/songs`, {
                    method: 'POST',
                    body: JSON.stringify({ song })
                });
                
                if (data.success) {
                    addToPlaylistModal.classList.add('hidden');
                    showNotification('Song added to playlist!', 'success');
                    
                    // Update current playlist if we're viewing it
                    if (currentPlaylist && currentPlaylist.id === playlistId) {
                        currentPlaylist.songs.push(song);
                        renderPlaylistSongs();
                    }
                    
                    // Update playlists
                    loadPlaylists();
                }
            } catch (error) {
                console.error('Failed to add song to playlist:', error);
                showNotification('Failed to add song to playlist', 'error');
            }
        }

        function showAddToPlaylistModal() {
            if (!currentSong) {
                showNotification('No song selected', 'error');
                return;
            }
            
            playlistsSelect.innerHTML = '';
            
            if (Object.keys(playlists).length === 0) {
                playlistsSelect.innerHTML = '<p class="text-gray-400 text-center py-4">No playlists yet</p>';
            } else {
                Object.values(playlists).forEach(playlist => {
                    const playlistOption = document.createElement('div');
                    playlistOption.className = 'p-3 rounded-lg hover:bg-white/10 cursor-pointer transition mb-2';
                    playlistOption.innerHTML = `
                        <div class="flex justify-between items-center">
                            <span class="text-ellipsis">${playlist.name}</span>
                            <span class="text-gray-400 text-sm">${playlist.songs.length} songs</span>
                        </div>
                    `;
                    playlistOption.addEventListener('click', () => addSongToPlaylist(playlist.id, currentSong));
                    playlistsSelect.appendChild(playlistOption);
                });
            }
            
            addToPlaylistModal.classList.remove('hidden');
        }

        // Authentication Functions
        async function submitAuthentication() {
            const jsonContent = browserJson.value.trim();
            
            if (!jsonContent) {
                showNotification('Please paste your browser.json content', 'error');
                return;
            }
            
            try {
                showLoading('Authenticating...');
                
                const data = await apiCall('/api/authenticate', {
                    method: 'POST',
                    body: JSON.stringify({ browserJson: jsonContent })
                });
                
                if (data.success) {
                    showNotification('Successfully authenticated!', 'success');
                    authModal.classList.add('hidden');
                    authBtn.innerHTML = '<i class="fas fa-user-check mr-2"></i>Signed In';
                    authBtnMobile.innerHTML = '<i class="fas fa-user-check"></i>';
                    browserJson.value = '';
                    
                    // Reload home data to get personalized recommendations
                    loadHomeData();
                } else {
                    throw new Error(data.error || 'Authentication failed');
                }
                
            } catch (error) {
                console.error('Authentication failed:', error);
                showNotification(`Authentication failed: ${error.message}`, 'error');
            } finally {
                hideLoading();
            }
        }

        // Data Management Functions
        async function exportData() {
            try {
                showLoading('Preparing export...');
                
                const response = await fetch('/api/export-data');
                if (!response.ok) throw new Error('Export failed');
                
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'musicgrab_export.json';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                
                showNotification('Data exported successfully', 'success');
                
            } catch (error) {
                console.error('Export failed:', error);
                showNotification('Export failed', 'error');
            } finally {
                hideLoading();
            }
        }

        async function importData(event) {
            const file = event.target.files[0];
            if (!file) return;
            
            try {
                showLoading('Importing data...');
                
                const formData = new FormData();
                formData.append('file', file);
                
                const response = await fetch('/api/import-data', {
                    method: 'POST',
                    body: formData
                });
                
                if (!response.ok) throw new Error('Import failed');
                
                const data = await response.json();
                
                if (data.success) {
                    showNotification('Data imported successfully', 'success');
                    
                    // Refresh all data
                    loadHomeData();
                    loadLibraryData();
                    loadPlaylists();
                    loadDownloadsData();
                } else {
                    throw new Error(data.error || 'Import failed');
                }
                
            } catch (error) {
                console.error('Import failed:', error);
                showNotification(`Import failed: ${error.message}`, 'error');
            } finally {
                hideLoading();
                // Reset file input
                importFile.value = '';
            }
        }
    </script>
</body>
</html>
