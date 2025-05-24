from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, send_file, current_app
import os
import uuid
from werkzeug.utils import secure_filename
import time
import subprocess
import shutil

converter_bp = Blueprint('converter', __name__)

@converter_bp.route('/mp4-to-mp3', methods=['GET', 'POST'])
def mp4_to_mp3():
    """MP4 to MP3 converter page"""
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'error')
            return jsonify({'success': False, 'error': 'No file part'})
        
        file = request.files['file']
        
        # If user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            flash('No selected file', 'error')
            return jsonify({'success': False, 'error': 'No selected file'})
        
        if file:
            # Create a unique ID for this conversion
            conversion_id = str(uuid.uuid4())
            temp_dir = os.path.join(current_app.config['TEMP_FOLDER'], conversion_id)
            os.makedirs(temp_dir, exist_ok=True)
            
            # Save the uploaded file
            filename = secure_filename(file.filename)
            file_path = os.path.join(temp_dir, filename)
            file.save(file_path)
            
            try:
                # Create a simple HTML file with instructions
                base_name = os.path.splitext(filename)[0]
                html_path = os.path.join(temp_dir, f"{base_name}_info.html")
                
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Media Conversion Note</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                        .container {{ max-width: 800px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
                        h1 {{ color: #1E3A8A; }}
                        .note {{ background-color: #f8f9fa; padding: 15px; border-left: 4px solid #0D9488; margin-bottom: 20px; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Your Media File: {filename}</h1>
                        <div class="note">
                            <p><strong>Note:</strong> Due to technical limitations in our deployment environment, we're unable to provide direct media conversion.</p>
                            <p>For best results, we recommend using one of these free alternatives:</p>
                            <ul>
                                <li>VLC Media Player (free, open-source)</li>
                                <li>Audacity (free, open-source)</li>
                                <li>Online converters like CloudConvert or Zamzar</li>
                            </ul>
                        </div>
                        <p>Your original file is included in this download for your convenience.</p>
                    </div>
                </body>
                </html>
                """
                
                # Write the HTML file
                with open(html_path, 'w') as f:
                    f.write(html_content)
                
                # Create a zip file with the original file and instructions
                output_filename = f"{base_name}_package.zip"
                output_path = os.path.join(temp_dir, output_filename)
                
                # Create zip file
                import zipfile
                with zipfile.ZipFile(output_path, 'w') as zipf:
                    zipf.write(file_path, arcname=filename)
                    zipf.write(html_path, arcname=f"{base_name}_info.html")
                
                return jsonify({
                    'success': True,
                    'conversion_id': conversion_id,
                    'filename': output_filename
                })
                
            except Exception as e:
                flash(f'Error during processing: {str(e)}', 'error')
                return jsonify({'success': False, 'error': str(e)})
    
    return render_template('converter/mp4_to_mp3.html')

@converter_bp.route('/mp3-to-mp4', methods=['GET', 'POST'])
def mp3_to_mp4():
    """MP3 to MP4 converter page"""
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'error')
            return jsonify({'success': False, 'error': 'No file part'})
        
        file = request.files['file']
        
        # If user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            flash('No selected file', 'error')
            return jsonify({'success': False, 'error': 'No selected file'})
        
        if file:
            # Create a unique ID for this conversion
            conversion_id = str(uuid.uuid4())
            temp_dir = os.path.join(current_app.config['TEMP_FOLDER'], conversion_id)
            os.makedirs(temp_dir, exist_ok=True)
            
            # Save the uploaded file
            filename = secure_filename(file.filename)
            file_path = os.path.join(temp_dir, filename)
            file.save(file_path)
            
            try:
                # Create a simple HTML file with instructions
                base_name = os.path.splitext(filename)[0]
                html_path = os.path.join(temp_dir, f"{base_name}_info.html")
                
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Media Conversion Note</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                        .container {{ max-width: 800px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
                        h1 {{ color: #1E3A8A; }}
                        .note {{ background-color: #f8f9fa; padding: 15px; border-left: 4px solid #0D9488; margin-bottom: 20px; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Your Media File: {filename}</h1>
                        <div class="note">
                            <p><strong>Note:</strong> Due to technical limitations in our deployment environment, we're unable to provide direct media conversion.</p>
                            <p>For best results, we recommend using one of these free alternatives:</p>
                            <ul>
                                <li>VLC Media Player (free, open-source)</li>
                                <li>Audacity (free, open-source)</li>
                                <li>Online converters like CloudConvert or Zamzar</li>
                            </ul>
                        </div>
                        <p>Your original file is included in this download for your convenience.</p>
                    </div>
                </body>
                </html>
                """
                
                # Write the HTML file
                with open(html_path, 'w') as f:
                    f.write(html_content)
                
                # Create a zip file with the original file and instructions
                output_filename = f"{base_name}_package.zip"
                output_path = os.path.join(temp_dir, output_filename)
                
                # Create zip file
                import zipfile
                with zipfile.ZipFile(output_path, 'w') as zipf:
                    zipf.write(file_path, arcname=filename)
                    zipf.write(html_path, arcname=f"{base_name}_info.html")
                
                return jsonify({
                    'success': True,
                    'conversion_id': conversion_id,
                    'filename': output_filename
                })
                
            except Exception as e:
                flash(f'Error during processing: {str(e)}', 'error')
                return jsonify({'success': False, 'error': str(e)})
    
    return render_template('converter/mp3_to_mp4.html')

@converter_bp.route('/download/<conversion_id>', methods=['GET'])
def download_converted_file(conversion_id):
    """Download the converted file"""
    try:
        # Get file from temp directory
        temp_dir = os.path.join(current_app.config['TEMP_FOLDER'], conversion_id)
        files = os.listdir(temp_dir)
        
        if not files:
            flash('File not found', 'error')
            return redirect(url_for('main.index'))
        
        file_path = os.path.join(temp_dir, files[0])
        file_name = files[0]
        
        # Send file to user
        return send_file(
            file_path,
            as_attachment=True,
            download_name=file_name
        )
        
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('main.index'))
