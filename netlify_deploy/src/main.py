import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, send_file
import os
import uuid
import time

# Import routes
from src.routes.main_routes import main_bp
from src.routes.file_routes import file_bp
from src.routes.qrcode_routes import qrcode_bp

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'toolbox_secret_key')

# Configure upload folder
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['TEMP_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(file_bp, url_prefix='/file')
app.register_blueprint(qrcode_bp, url_prefix='/qrcode')

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
