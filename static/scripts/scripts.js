document.getElementById('uploadForm').addEventListener('submit', (e) => {
    const fileInput = document.getElementById('fileInput');
    if (!fileInput.files.length) {
        e.preventDefault();
        alert('Please select a file to upload.');
    }
});

function loadVideo() {
    const videoSelect = document.getElementById('videoSelect');
    const videoPlayer = document.getElementById('videoPlayer');
    const videoSource = document.getElementById('videoSource');

    // Get the selected video filename
    const selectedVideo = videoSelect.value;

    // Update the video player's source URL
    videoSource.src = `/media/play/${selectedVideo}`;
    console.log(`Loading video from: ${videoSource.src}`);
    videoPlayer.load(); // Reload the video
}

async function fetchAndDisplayVideos() {
    const videosContainer = document.getElementById('videosContainer');

    try {
        const response = await fetch('/media/my_videos');
        const videos = await response.json();

        videosContainer.innerHTML = '';
        videos.forEach(video => {
            const videoDiv = document.createElement('div');
            videoDiv.className = 'videoItem';

            const videoPlayer = document.createElement('video');
            videoPlayer.controls = true;
            videoPlayer.src = `/media/play/${video.filename}`;
            videoPlayer.width = 300;

            const videoTitle = document.createElement('p');
            videoTitle.textContent = video.title || video.filename;

            const videoDescription = document.createElement('p');
            videoDescription.textContent = video.description || 'No description available';

            videoDiv.appendChild(videoPlayer);
            videoDiv.appendChild(videoTitle);
            videoDiv.appendChild(videoDescription);
            videosContainer.appendChild(videoDiv);
        });
    } catch (error) {
        console.error('Error fetching videos:', error);
    }
}
// async function fetchAndDisplayVideos() {
//     const videosContainer = document.getElementById('videosContainer');

//     try {
//         const response = await fetch('/media/list_videos'); // Fetch video list
//         const videos = await response.json();

//         // Clear existing videos to avoid duplicates
//         videosContainer.innerHTML = '';

//         // Dynamically create video elements
//         videos.forEach(video => {
//             const videoDiv = document.createElement('div');
//             videoDiv.className = 'videoItem';

//             const videoPlayer = document.createElement('video');
//             videoPlayer.controls = true; // Add playback controls
//             videoPlayer.src = `/media/play/${video}`; // Set video source
//             videoPlayer.width = 300; // Set video width (optional)

//             const videoTitle = document.createElement('p');
//             videoTitle.textContent = video; // Display video filename

//             videoDiv.appendChild(videoPlayer);
//             videoDiv.appendChild(videoTitle);
//             videosContainer.appendChild(videoDiv);
//         });
//     } catch (error) {
//         console.error('Error fetching videos:', error);
//     }
// }

// Run fetchAndDisplayVideos on page load
window.onload = fetchAndDisplayVideos;

// Run fetchVideos on page load
window.onload = fetchVideos;