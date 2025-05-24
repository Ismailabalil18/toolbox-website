import base64

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, send_file, current_app
import os
import uuid
from werkzeug.utils import secure_filename
import time
import io
import zipfile

file_bp = Blueprint('file', __name__)

@file_bp.route('/compressor', methods=['GET', 'POST'])
def compressor():
    """File compressor page"""
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
            try:
                # Get compression level
                compression_level = int(request.form.get('compression_level', 6))  # Default medium compression
                
                # Read file into memory
                file_data = file.read()
                filename = secure_filename(file.filename)
                
                # Create a zip file in memory
                memory_file = io.BytesIO()
                with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED, compresslevel=compression_level) as zipf:
                    zipf.writestr(filename, file_data)
                
                # Get file sizes for comparison
                original_size = len(file_data)
                memory_file.seek(0)
                compressed_size = len(memory_file.getvalue())
                
                # Generate a unique ID for this compression
                compression_id = str(uuid.uuid4())
                
                # Return the compressed data directly in the response
                return jsonify({
                    'success': True,
                    'original_size': original_size,
                    'compressed_size': compressed_size,
                    'reduction_percent': round((1 - (compressed_size / original_size)) * 100, 2) if original_size > 0 else 0,
                    'filename': os.path.splitext(filename)[0] + '_compressed.zip',
                    'compressed_data': base64.b64encode(memory_file.getvalue()).decode('utf-8')
                })
                
            except Exception as e:
                flash(f'Error during compression: {str(e)}', 'error')
                return jsonify({'success': False, 'error': str(e)})
    
    return render_template('file/compressor.html')
