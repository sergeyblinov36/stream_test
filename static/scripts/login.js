document.getElementById('loginForm').onsubmit = async function(event) {
    event.preventDefault(); // Prevent the page from refreshing

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        const messageElement = document.getElementById('loginMessage');

        if (response.status === 200) {
            const token = data.token; // JWT token received
            localStorage.setItem('authToken', token); // Save token locally

            messageElement.style.color = 'green';
            messageElement.textContent = 'Login successful! Redirecting...';

            // Redirect to another page
            setTimeout(() => {
                window.location.href = '/media/my_videos'; // Replace with your target page
            }, 1000);
        } else {
            // Display error message
            messageElement.style.color = 'red';
            messageElement.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        console.error('Error during login:', error);
        document.getElementById('loginMessage').textContent = 'An unexpected error occurred.';
    }
};