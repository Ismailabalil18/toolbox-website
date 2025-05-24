from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, send_file, current_app
import os
import uuid
from werkzeug.utils import secure_filename
import time
import io
import zipfile

pdf_bp = Blueprint('pdf', __name__)

@pdf_bp.route('/pdf-to-word', methods=['GET', 'POST'])
def pdf_to_word():
    """PDF to Word converter page"""
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
        
        # Check if the file is a PDF
        if file and file.filename.lower().endswith('.pdf'):
            # Create a unique ID for this conversion
            conversion_id = str(uuid.uuid4())
            temp_dir = os.path.join(current_app.config['TEMP_FOLDER'], conversion_id)
            os.makedirs(temp_dir, exist_ok=True)
            
            # Save the uploaded file
            filename = secure_filename(file.filename)
            pdf_path = os.path.join(temp_dir, filename)
            file.save(pdf_path)
            
            try:
                # Instead of converting PDF to Word directly (which requires native dependencies),
                # we'll create a simple HTML file explaining the limitation and provide the original PDF
                base_name = os.path.splitext(filename)[0]
                html_path = os.path.join(temp_dir, f"{base_name}.html")
                
                # Create a simple HTML file with instructions
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>PDF Conversion Note</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                        .container {{ max-width: 800px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
                        h1 {{ color: #1E3A8A; }}
                        .note {{ background-color: #f8f9fa; padding: 15px; border-left: 4px solid #0D9488; margin-bottom: 20px; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Your PDF File: {filename}</h1>
                        <div class="note">
                            <p><strong>Note:</strong> Due to technical limitations in our deployment environment, we're unable to provide direct PDF to Word conversion.</p>
                            <p>For best results, we recommend using one of these alternatives:</p>
                            <ul>
                                <li>Microsoft Office Online (free with Microsoft account)</li>
                                <li>Google Docs (free with Google account)</li>
                                <li>Adobe Acrobat Online (limited free conversions)</li>
                            </ul>
                        </div>
                        <p>Your original PDF file is included in this download for your convenience.</p>
                    </div>
                </body>
                </html>
                """
                
                # Write the HTML file
                with open(html_path, 'w') as f:
                    f.write(html_content)
                
                # Create a zip file containing both the HTML and the original PDF
                zip_path = os.path.join(temp_dir, f"{base_name}_package.zip")
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    zipf.write(pdf_path, arcname=filename)
                    zipf.write(html_path, arcname=f"{base_name}.html")
                
                return jsonify({
                    'success': True,
                    'conversion_id': conversion_id,
                    'filename': f"{base_name}_package.zip"
                })
                
            except Exception as e:
                flash(f'Error during processing: {str(e)}', 'error')
                return jsonify({'success': False, 'error': str(e)})
        else:
            flash('Please upload a PDF file', 'error')
            return jsonify({'success': False, 'error': 'Invalid file format. Please upload a PDF file.'})
    
    return render_template('pdf/pdf_to_word.html')

@pdf_bp.route('/download/<conversion_id>', methods=['GET'])
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
