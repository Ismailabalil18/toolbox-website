from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Homepage"""
    # Define tools to display on homepage - only showing File Compressor and QR Code Generator
    tools = [
        {
            'name': 'File Compressor',
            'description': 'Compress files to reduce size',
            'url': url_for('file.compressor'),
            'icon': 'archive'
        },
        {
            'name': 'QR Code Generator',
            'description': 'Generate QR codes from text or URLs',
            'url': url_for('qrcode.generator'),
            'icon': 'qr-code'
        }
    ]
    return render_template('index.html', tools=tools)

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@main_bp.route('/faq')
def faq():
    """FAQ page"""
    return render_template('faq.html', title="Frequently Asked Questions")

@main_bp.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html', title="Contact Us")

@main_bp.route('/privacy')
def privacy():
    """Privacy policy page"""
    return render_template('privacy.html', title="Privacy Policy")

@main_bp.route('/terms')
def terms():
    """Terms of service page"""
    return render_template('terms.html', title="Terms of Service")
