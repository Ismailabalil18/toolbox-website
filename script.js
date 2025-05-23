document.addEventListener('DOMContentLoaded', () => {
    const downloadBtn = document.getElementById('downloadBtn');
    const videoUrlInput = document.getElementById('videoUrl');
    const statusDiv = document.getElementById('status');
    const contactForm = document.getElementById('contactForm');

    // Add loading state to button
    function setLoading(isLoading) {
        const button = downloadBtn;
        const icon = button.querySelector('i');
        const text = button.querySelector('span');

        if (isLoading) {
            button.disabled = true;
            icon.className = 'fas fa-spinner fa-spin';
            text.textContent = 'Processing...';
        } else {
            button.disabled = false;
            icon.className = 'fas fa-download';
            text.textContent = 'Download';
        }
    }

    // Validate YouTube URL
    function isValidYouTubeUrl(url) {
        const pattern = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$/;
        return pattern.test(url);
    }

    // Handle video download
    downloadBtn.addEventListener('click', async () => {
        const videoUrl = videoUrlInput.value.trim();
        
        if (!videoUrl) {
            showStatus('Please enter a video URL', 'error');
            videoUrlInput.focus();
            return;
        }

        if (!isValidYouTubeUrl(videoUrl)) {
            showStatus('Please enter a valid YouTube URL', 'error');
            videoUrlInput.focus();
            return;
        }

        try {
            setLoading(true);
            showStatus('Processing your request...', 'info');

            const response = await fetch('/api/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: videoUrl })
            });

            const data = await response.json();

            if (response.ok) {
                showStatus('Download started!', 'success');
                // Trigger download
                window.location.href = data.downloadUrl;
            } else {
                throw new Error(data.message || 'Download failed');
            }
        } catch (error) {
            console.error('Download error:', error);
            if (error.message.includes('Failed to fetch')) {
                showStatus('Server is not running. Please start the server first.', 'error');
            } else {
                showStatus(error.message, 'error');
            }
        } finally {
            setLoading(false);
        }
    });

    // Handle contact form submission
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const submitButton = contactForm.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;
        
        try {
            // Show loading state
            submitButton.disabled = true;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

            const formData = new FormData(contactForm);
            const data = {
                email: formData.get('email'),
                message: formData.get('message')
            };

            const response = await fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                showStatus('Message sent successfully!', 'success');
                contactForm.reset();
            } else {
                throw new Error(result.message || 'Failed to send message');
            }
        } catch (error) {
            console.error('Contact form error:', error);
            if (error.message.includes('Failed to fetch')) {
                showStatus('Server is not running. Please start the server first.', 'error');
            } else {
                showStatus(error.message, 'error');
            }
        } finally {
            // Reset button state
            submitButton.disabled = false;
            submitButton.innerHTML = originalText;
        }
    });

    // Helper function to show status messages
    function showStatus(message, type) {
        statusDiv.textContent = message;
        statusDiv.className = `status ${type}`;
        statusDiv.style.display = 'block';
        
        // Hide status message after 5 seconds
        setTimeout(() => {
            statusDiv.style.display = 'none';
        }, 5000);
    }

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Focus input on page load
    videoUrlInput.focus();
}); 