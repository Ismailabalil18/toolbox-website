from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, send_file, current_app
import os
import uuid
from werkzeug.utils import secure_filename
import time
import random
import base64
import io
from urllib.request import urlopen
import json

image_bp = Blueprint('image', __name__)

@image_bp.route('/generator', methods=['GET', 'POST'])
def generator():
    """Image generator page"""
    if request.method == 'POST':
        try:
            # Get prompt from form
            prompt = request.form.get('prompt', '')
            if not prompt:
                flash('Please enter a prompt', 'error')
                return jsonify({'success': False, 'error': 'No prompt provided'})
            
            # Get style and size options
            style = request.form.get('style', 'realistic')
            size = request.form.get('size', '512x512')
            
            # Create a unique ID for this generation
            generation_id = str(uuid.uuid4())
            temp_dir = os.path.join(current_app.config['TEMP_FOLDER'], generation_id)
            os.makedirs(temp_dir, exist_ok=True)
            
            # Parse size
            width, height = map(int, size.split('x'))
            
            # Generate a procedural image based on the prompt
            # This is a pure Python implementation without native dependencies
            
            # Create a simple SVG with random shapes based on the prompt
            svg_content = []
            svg_content.append(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">')
            
            # Add background
            background_color = "#f0f0f0"
            svg_content.append(f'<rect width="{width}" height="{height}" fill="{background_color}"/>')
            
            # Generate some random shapes based on the hash of the prompt
            seed = hash(prompt + style)
            random.seed(seed)
            
            # Generate shapes based on style
            shape_count = 20
            
            for i in range(shape_count):
                x1 = random.randint(0, width)
                y1 = random.randint(0, height)
                size = random.randint(20, 100)
                
                # Generate colors based on style
                if style == 'realistic':
                    r = random.randint(0, 200)
                    g = random.randint(0, 200)
                    b = random.randint(0, 200)
                elif style == 'cartoon':
                    r = random.randint(100, 255)
                    g = random.randint(100, 255)
                    b = random.randint(100, 255)
                elif style == 'abstract':
                    r = random.randint(50, 255)
                    g = random.randint(50, 255)
                    b = random.randint(50, 255)
                else:  # Default
                    r = random.randint(0, 255)
                    g = random.randint(0, 255)
                    b = random.randint(0, 255)
                
                color = f"rgb({r},{g},{b})"
                opacity = random.uniform(0.3, 0.8)
                
                # Choose a random shape
                shape_type = random.choice(['circle', 'rect', 'ellipse'])
                
                if shape_type == 'circle':
                    svg_content.append(f'<circle cx="{x1}" cy="{y1}" r="{size/2}" fill="{color}" opacity="{opacity:.1f}" />')
                elif shape_type == 'rect':
                    svg_content.append(f'<rect x="{x1}" y="{y1}" width="{size}" height="{size}" fill="{color}" opacity="{opacity:.1f}" />')
                else:  # ellipse
                    svg_content.append(f'<ellipse cx="{x1}" cy="{y1}" rx="{size}" ry="{size/2}" fill="{color}" opacity="{opacity:.1f}" />')
            
            # Add some text with the prompt
            svg_content.append(f'<text x="{width/2}" y="{height-20}" text-anchor="middle" font-family="Arial" font-size="16">{prompt}</text>')
            
            # Close SVG
            svg_content.append('</svg>')
            
            # Join all SVG content
            svg_data = ''.join(svg_content)
            
            # Save the generated SVG
            output_filename = f"generated_image_{generation_id}.svg"
            output_path = os.path.join(temp_dir, output_filename)
            
            with open(output_path, 'w') as f:
                f.write(svg_data)
            
            return jsonify({
                'success': True,
                'generation_id': generation_id,
                'filename': output_filename
            })
            
        except Exception as e:
            flash(f'Error during image generation: {str(e)}', 'error')
            return jsonify({'success': False, 'error': str(e)})
    
    return render_template('image/generator.html')

@image_bp.route('/download/<generation_id>', methods=['GET'])
def download_generated_image(generation_id):
    """Download the generated image"""
    try:
        # Get file from temp directory
        temp_dir = os.path.join(current_app.config['TEMP_FOLDER'], generation_id)
        files = os.listdir(temp_dir)
        
        if not files:
            flash('Image not found', 'error')
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
        flash(f'Error downloading image: {str(e)}', 'error')
        return redirect(url_for('main.index'))
