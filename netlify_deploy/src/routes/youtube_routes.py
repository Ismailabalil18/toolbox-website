from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, send_file, current_app
import os
import uuid
from werkzeug.utils import secure_filename
import time
import requests
import json
import zipfile
import io

youtube_bp = Blueprint('youtube', __name__)

@youtube_bp.route('/downloader', methods=['GET', 'POST'])
def downloader():
    """YouTube video downloader page"""
    if request.method == 'POST':
        try:
            # Get YouTube URL from form
            youtube_url = request.form.get('youtube_url', '')
            if not youtube_url:
                flash('Please enter a YouTube URL', 'error')
                return jsonify({'success': False, 'error': 'No YouTube URL provided'})
            
            # Create a unique ID for this download
            download_id = str(uuid.uuid4())
            temp_dir = os.path.join(current_app.config['TEMP_FOLDER'], download_id)
            os.makedirs(temp_dir, exist_ok=True)
            
            # Create a simple HTML file with instructions
            html_path = os.path.join(temp_dir, "youtube_info.html")
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>YouTube Download Note</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                    .container {{ max-width: 800px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
                    h1 {{ color: #1E3A8A; }}
                    .note {{ background-color: #f8f9fa; padding: 15px; border-left: 4px solid #0D9488; margin-bottom: 20px; }}
                    .url {{ word-break: break-all; background: #eee; padding: 10px; border-radius: 4px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>YouTube Download Request</h1>
                    <div class="note">
                        <p><strong>Note:</strong> Due to technical limitations in our deployment environment, we're unable to provide direct YouTube video downloads.</p>
                        <p>For best results, we recommend using one of these free alternatives:</p>
                        <ul>
                            <li>VLC Media Player (free, open-source)</li>
                            <li>YouTube-DL (free, open-source command line tool)</li>
                            <li>Browser extensions like Video DownloadHelper</li>
                        </ul>
                    </div>
                    <p>Your requested YouTube URL was:</p>
                    <p class="url">{youtube_url}</p>
                </div>
            </body>
            </html>
            """
            
            # Write the HTML file
            with open(html_path, 'w') as f:
                f.write(html_content)
            
            # Create a text file with the YouTube URL
            url_file_path = os.path.join(temp_dir, "youtube_url.txt")
            with open(url_file_path, 'w') as f:
                f.write(f"YouTube URL: {youtube_url}\n\n")
                f.write("Due to technical limitations, we cannot provide direct downloads.\n")
                f.write("Please use a dedicated tool like youtube-dl or a browser extension.")
            
            # Create a zip file with the information
            output_filename = f"youtube_info_{download_id}.zip"
            output_path = os.path.join(temp_dir, output_filename)
            
            with zipfile.ZipFile(output_path, 'w') as zipf:
                zipf.write(html_path, arcname="youtube_info.html")
                zipf.write(url_file_path, arcname="youtube_url.txt")
            
            return jsonify({
                'success': True,
                'download_id': download_id,
                'filename': output_filename
            })
            
        except Exception as e:
            flash(f'Error processing request: {str(e)}', 'error')
            return jsonify({'success': False, 'error': str(e)})
    
    return render_template('youtube/downloader.html')

@youtube_bp.route('/download/<download_id>', methods=['GET'])
def download_video(download_id):
    """Download the processed YouTube information"""
    try:
        temp_dir = os.path.join(current_app.config['TEMP_FOLDER'], download_id)
        
        # Find the zip file in the temp directory
        for filename in os.listdir(temp_dir):
            if filename.endswith('.zip'):
                file_path = os.path.join(temp_dir, filename)
                return send_file(file_path, as_attachment=True)
        
        flash('File not found', 'error')
        return redirect(url_for('youtube.downloader'))
    except Exception as e:
        flash(f'Error during download: {str(e)}', 'error')
        return redirect(url_for('youtube.downloader'))
