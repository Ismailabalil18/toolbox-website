from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, send_file, current_app
import os
import uuid
from werkzeug.utils import secure_filename
import time
import io
import zipfile

qrcode_bp = Blueprint('qrcode', __name__)

@qrcode_bp.route('/generator', methods=['GET', 'POST'])
def generator():
    """QR Code Generator page"""
    if request.method == 'POST':
        try:
            # Get content for QR code
            content = request.form.get('content', '')
            if not content:
                flash('Please enter content for the QR code', 'error')
                return jsonify({'success': False, 'error': 'No content provided'})
            
            # Create a unique ID for this QR code
            qr_id = str(uuid.uuid4())
            
            # Generate a simple HTML file with embedded QR code using JavaScript
            # This avoids any native dependencies completely
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>QR Code</title>
                <script src="https://cdn.jsdelivr.net/npm/qrcode@1.5.1/build/qrcode.min.js"></script>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; text-align: center; }}
                    .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
                    h1 {{ color: #1E3A8A; }}
                    .qr-container {{ margin: 30px auto; }}
                    .content {{ background-color: #f8f9fa; padding: 15px; border-left: 4px solid #0D9488; margin: 20px 0; text-align: left; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Your QR Code</h1>
                    <div class="qr-container">
                        <canvas id="qrcode"></canvas>
                    </div>
                    <h3>Encoded Content:</h3>
                    <div class="content">
                        {content}
                    </div>
                    <p>Scan with any QR code reader to access your content</p>
                </div>
                <script>
                    window.onload = function() {{
                        QRCode.toCanvas(document.getElementById('qrcode'), "{content.replace('"', '"')}", {{
                            width: 300,
                            margin: 2,
                            color: {{
                                dark: '#000000',
                                light: '#ffffff'
                            }}
                        }}, function(error) {{
                            if (error) console.error(error);
                        }});
                    }};
                </script>
            </body>
            </html>
            """
            
            return jsonify({
                'success': True,
                'qr_id': qr_id,
                'content': content,
                'html': html_content
            })
            
        except Exception as e:
            flash(f'Error generating QR code: {str(e)}', 'error')
            return jsonify({'success': False, 'error': str(e)})
    
    return render_template('qrcode/generator.html')

@qrcode_bp.route('/view/<qr_id>', methods=['GET'])
def view_qrcode(qr_id):
    """View the generated QR code - simplified to avoid file system operations"""
    # In production, we'll just redirect to the generator page
    # since we can't rely on temp file storage
    return redirect(url_for('qrcode.generator'))
