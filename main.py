const handleDownload = async (song) => {
    setDownloading(song.id);
    try {
        const payload = {
            videoId: song.id,
            title: song.title,
            artist: song.artist,
            album: song.album || '',
            thumbnail: song.thumbnail || '',
            format: 'mp3'
        };
        console.log('Download payload:', payload);

        const response = await fetch(`${API_BASE}/api/download`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Download failed');
        }

        const data = await response.json();
        if (data.status === 'success') {
            const cleanFilename = `${song.artist} - ${song.title}.mp3`.replace(/[<>:"/\\|?*]/g, '');
            const link = document.createElement('a');
            link.href = `${API_BASE}${data.downloadUrl}`;
            link.download = cleanFilename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            showMessage(`✅ "${song.title}" downloaded!`, 'success');
            await Promise.all([loadSongs(), loadArtists()]);
        } else {
            throw new Error(data.error || 'Download failed');
        }
    } catch (error) {
        console.error('Download error:', error);
        showMessage(`❌ ${error.message}`, 'error');
    } finally {
        setDownloading(null);
    }
};
