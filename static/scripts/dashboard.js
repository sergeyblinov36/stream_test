document.addEventListener('DOMContentLoaded', () => {
    // Select all delete buttons
    const deleteButtons = document.querySelectorAll('.delete-button');

    // Attach click event listeners to each delete button
    deleteButtons.forEach(button => {
        button.addEventListener('click', async (event) => {
            const videoId = event.target.getAttribute('data-video-id');

            const confirmation = confirm('Are you sure you want to delete this video?');
            if (!confirmation) return;

            try {
                const response = await fetch(`/delete_video/${videoId}`, { method: 'DELETE' });
                const result = await response.json();

                if (response.ok) {
                    alert(result.message);
                    // Remove the video element from the UI
                    document.getElementById(`video-${videoId}`).remove();
                } else {
                    alert(result.error || 'Failed to delete the video.');
                }
            } catch (error) {
                console.error('Error deleting video:', error);
                alert('An unexpected error occurred.');
            }
        });
    });
});