const express = require('express');
const cors = require('cors');
const path = require('path');
const { downloadVideo } = require('./utils/downloader');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Serve static files
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// API Routes
app.post('/api/download', async (req, res) => {
    try {
        const { url } = req.body;
        
        if (!url) {
            return res.status(400).json({ message: 'URL is required' });
        }

        const downloadUrl = await downloadVideo(url);
        res.json({ downloadUrl });
    } catch (error) {
        console.error('Download error:', error);
        res.status(500).json({ message: error.message || 'Failed to process video download' });
    }
});

app.post('/api/contact', (req, res) => {
    try {
        const { email, message } = req.body;
        
        if (!email || !message) {
            return res.status(400).json({ message: 'Email and message are required' });
        }

        // Here you would typically send an email or store the message
        // For now, we'll just log it
        console.log('Contact form submission:', { email, message });
        
        res.json({ message: 'Message received successfully' });
    } catch (error) {
        console.error('Contact form error:', error);
        res.status(500).json({ message: 'Failed to process contact form' });
    }
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ message: 'Something went wrong!' });
});

// Start server
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
}); 