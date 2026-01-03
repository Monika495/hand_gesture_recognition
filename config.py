"""
config.py - Application Configuration
UPDATED: More lenient threshold for better detection
"""
import os

class Config:
    SECRET_KEY = 'your-secret-key-change-in-production'
    
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///gesture_validation.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Validation settings - MORE LENIENT
    DEFAULT_THRESHOLD = 0.35  # Much more lenient for better detection
    MIN_CONFIDENCE = 50.0  # Lower minimum confidence

# Create instance
config = Config()