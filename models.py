"""
models.py - Fixed with proper sample_count property
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    gestures = db.relationship('Gesture', backref='user', lazy=True, cascade='all, delete-orphan')
    validation_logs = db.relationship('ValidationLog', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Gesture(db.Model):
    __tablename__ = 'gestures'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    samples = db.relationship('GestureSample', backref='gesture', lazy=True, cascade='all, delete-orphan')
    
    @property
    def sample_count(self):
        """FIXED: Proper count of samples"""
        return len(self.samples) if self.samples else 0

class GestureSample(db.Model):
    __tablename__ = 'gesture_samples'
    
    id = db.Column(db.Integer, primary_key=True)
    gesture_id = db.Column(db.Integer, db.ForeignKey('gestures.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    landmarks_json = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def landmarks(self):
        return json.loads(self.landmarks_json)
    
    @landmarks.setter
    def landmarks(self, value):
        self.landmarks_json = json.dumps(value)

class ValidationLog(db.Model):
    __tablename__ = 'validation_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    detected_gesture = db.Column(db.String(100))
    expected_gestures = db.Column(db.Text)
    
    is_correct = db.Column(db.Boolean, nullable=False)
    distance = db.Column(db.Float)
    threshold_used = db.Column(db.Float)
    
    session_id = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    @property
    def expected_gestures_list(self):
        if self.expected_gestures:
            return json.loads(self.expected_gestures)
        return []