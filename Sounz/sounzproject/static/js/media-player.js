document.addEventListener('DOMContentLoaded', function() {
    const mediaPlayers = document.querySelectorAll('.media-player-container');
    
    mediaPlayers.forEach(initializeMediaPlayer);
    
    function initializeMediaPlayer(container) {
        // Elements
        const videoEl = container.querySelector('#media-video');
        const audioEl = container.querySelector('#media-audio');
        const playPauseBtn = container.querySelector('#play-pause-btn');
        const currentTimeEl = container.querySelector('#current-time');
        const durationEl = container.querySelector('#duration');
        const progressFill = container.querySelector('#progress-fill');
        const progressBar = container.querySelector('.progress-bar');
        
        // Media type from Django data attributes
        const mediaType = container.dataset.mediaType; // 'video' or 'audio'
        
        // Set the current media element based on type
        const currentMedia = mediaType === 'Video' ? videoEl : audioEl;
        
        // State
        let isPlaying = true;
        
        // Play/Pause button icon
        const playIcon = '<svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="15" cy="15" r="15" fill="#D4D4D4"/><path d="M21.5996 14.284C22.2663 14.6689 22.2663 15.6312 21.5996 16.0161L12.6746 21.1689C12.0079 21.5538 11.1746 21.0727 11.1746 20.3029L11.1746 9.99722C11.1746 9.22742 12.0079 8.7463 12.6746 9.1312L21.5996 14.284Z" fill="#3C3C3C"/></svg>';
        const pauseIcon = '<svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="15" cy="15" r="15" fill="#D4D4D4"/><rect x="10" y="9" width="2.77778" height="11" rx="1" fill="#3F3F3F"/><rect x="17.2222" y="9" width="2.77778" height="11" rx="1" fill="#3F3F3F"/></svg>';
        
        // Format time (seconds to MM:SS)
        function formatTime(seconds) {
            if (isNaN(seconds)) return "0:00";
            const minutes = Math.floor(seconds / 60);
            const remainingSeconds = Math.floor(seconds % 60);
            return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
        }
        
        // Update play/pause button icon
        function updatePlayPauseBtn() {
            playPauseBtn.innerHTML = isPlaying ? pauseIcon : playIcon;
        }
        document.addEventListener("keydown", function (event) {
            var popup = document.getElementById("popup");
        
            var isPopupVisible = popup.classList.contains("show");
        
            if (!isPopupVisible && event.code === "Space") {
                event.preventDefault();
                togglePlay(); 
            }
        });
        // Play/Pause
        function togglePlay() {
            if (!currentMedia) return;
            
            if (isPlaying) {
                currentMedia.pause();
            } else {
                currentMedia.play().catch(error => {
                    console.error("Error playing media:", error);
                });
            }
            
            isPlaying = !isPlaying;
            updatePlayPauseBtn();
        }
        
        // Time update
        function updateTime() {
            const currentTime = currentMedia.currentTime;
            const duration = currentMedia.duration || 0;
            
            // Update time display
            currentTimeEl.textContent = formatTime(currentTime);
            durationEl.textContent = formatTime(duration);
            
            // Update progress bar
            const progress = (currentTime / duration) * 100;
            progressFill.style.width = `${progress}%`;
        }
        
        // Seek
        function seek(event) {
            if (!currentMedia || !currentMedia.duration || !currentMedia.seekable.length) return;
        
            const rect = progressBar.getBoundingClientRect();
            const pos = (event.clientX - rect.left) / rect.width;
        
            // Get the seekable range
            const seekableStart = currentMedia.seekable.start(0);
            const seekableEnd = currentMedia.seekable.end(0);
        
            // Ensure new time is within the valid range
            const newTime = Math.max(seekableStart, Math.min(pos * currentMedia.duration, seekableEnd));
        
            console.log(`Seeking to: ${newTime} (Valid Range: ${seekableStart} - ${seekableEnd})`);
        
            currentMedia.currentTime = newTime;
        }
        
        // Event listeners
        playPauseBtn.addEventListener('click', togglePlay);
        
        // Fix for seeking: Add both click and pointer events
        progressBar.addEventListener('click', seek);
        progressBar.addEventListener('mousedown', (event) => {
            seek(event);
        
            const handleMouseMove = (event) => seek(event);
            const handleMouseUp = () => {
                document.removeEventListener('mousemove', handleMouseMove);
                document.removeEventListener('mouseup', handleMouseUp);
            };
        
            document.addEventListener('mousemove', handleMouseMove);
            document.addEventListener('mouseup', handleMouseUp);
        });
        
        // Media events
        currentMedia.addEventListener('timeupdate', updateTime);
        
        currentMedia.addEventListener('ended', () => {
            isPlaying = false;
            updatePlayPauseBtn();
        });
        
        // Preload metadata
        currentMedia.addEventListener('loadedmetadata', () => {
            durationEl.textContent = formatTime(currentMedia.duration);
        });
        
        // Handle errors
        currentMedia.addEventListener('error', (e) => {
            console.error("Media error:", e);
        });
        audioEl.addEventListener('loadedmetadata', () => {
            console.log("Metadata loaded. Duration:", audioEl.duration);
            
            // Now seeking should work
            audioEl.currentTime = 10;
        });
    }
});