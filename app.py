"""
app.py - COMPLETE PROFESSIONAL GESTURE VALIDATION SYSTEM
✅ More lenient detection (0.35 threshold)
✅ Small corner indicator
✅ ALL validations stored in database
✅ Manage gestures page (view/delete images)
✅ Complete validation logs
✅ 2-hand support
✅ Enhanced validation with save/don't save options
✅ Better gesture discrimination
✅ Fixed dashboard stats
✅ Working gesture deletion
"""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from datetime import datetime, timedelta
import json
import uuid
import traceback


from config import config
from models import db, User, Gesture, GestureSample, ValidationLog
from utils.gesture_processor import GestureProcessor
from utils.validator import validate_against_multiple_gestures

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

# ===========================================
# AUTH ROUTES
# ===========================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not username or not email or not password:
            flash('All fields required', 'danger')
            return redirect(url_for('signup'))
        
        if len(password) < 6:
            flash('Password must be 6+ characters', 'danger')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(username=username).first():
            flash('Username taken', 'danger')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(email=email).first():
            flash('Email registered', 'danger')
            return redirect(url_for('signup'))
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('✅ Account created! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Enter credentials', 'danger')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('index'))

# ===========================================
# MAIN ROUTES
# ===========================================

# Replace the /dashboard route in app.py with this fixed version

@app.route('/dashboard')
@login_required
def dashboard():
    """Fixed dashboard with correct validation count"""
    gestures = Gesture.query.filter_by(user_id=current_user.id).all()
    
    # Calculate stats
    total_gestures = len(gestures)
    total_samples = sum(gesture.sample_count for gesture in gestures)
    
    # FIXED: Get ALL validations count (not limited to 50)
    total_validations = ValidationLog.query.filter_by(
        user_id=current_user.id
    ).count()
    
    # Get recent validations for accuracy calculation (last 100)
    recent_logs = ValidationLog.query.filter_by(
        user_id=current_user.id
    ).order_by(
        ValidationLog.timestamp.desc()
    ).limit(100).all()
    
    if recent_logs:
        correct_count = sum(1 for log in recent_logs if log.is_correct)
        accuracy = round((correct_count / len(recent_logs)) * 100, 1)
    else:
        accuracy = 0
    
    # Get only 5 recent logs for dashboard display
    recent_logs_display = recent_logs[:5]
    
    return render_template('dashboard.html',
                         gestures=gestures,
                         total_gestures=total_gestures,
                         total_samples=total_samples,
                         total_validations=total_validations,  # Now shows actual count
                         accuracy=accuracy,
                         recent_logs=recent_logs_display)

@app.route('/upload_gesture', methods=['GET', 'POST'])
@login_required
def upload_gesture():
    if request.method == 'POST':
        gesture_name = request.form.get('gesture_name', '').strip().lower()
        
        if not gesture_name:
            flash('Enter gesture name', 'danger')
            return redirect(url_for('upload_gesture'))
        
        if 'file' not in request.files:
            flash('No file', 'danger')
            return redirect(url_for('upload_gesture'))
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(url_for('upload_gesture'))
        
        if not allowed_file(file.filename):
            flash('Invalid file type', 'danger')
            return redirect(url_for('upload_gesture'))
        
        try:
            filename = f"{current_user.id}_{gesture_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            file.save(filepath)
            
            processor = GestureProcessor()
            landmarks = processor.process_image(filepath)
            
            if landmarks is None or len(landmarks) != 21:
                os.remove(filepath)
                flash('❌ No hand detected in image', 'danger')
                return redirect(url_for('upload_gesture'))
            
            # Find or create gesture
            gesture = Gesture.query.filter_by(
                user_id=current_user.id,
                name=gesture_name
            ).first()
            
            if not gesture:
                gesture = Gesture(
                    user_id=current_user.id,
                    name=gesture_name,
                    description=f"Created {datetime.now().strftime('%Y-%m-%d')}"
                )
                db.session.add(gesture)
                db.session.flush()
            
            # Create sample
            sample = GestureSample(
                gesture_id=gesture.id,
                image_path=filename,
                landmarks=landmarks
            )
            db.session.add(sample)
            db.session.commit()
            
            # Warn if less than 3 samples
            if len(gesture.samples) < 3:
                flash(f'⚠️ For better accuracy, upload at least 3 samples for "{gesture_name}"', 'warning')
            
            flash(f'✅ "{gesture_name}" uploaded! Total samples: {len(gesture.samples)}', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            flash(f'❌ Error: {str(e)}', 'danger')
            if 'filepath' in locals() and os.path.exists(filepath):
                os.remove(filepath)
            return redirect(url_for('upload_gesture'))
    
    return render_template('upload_gesture.html')

@app.route('/manage_gestures')
@login_required
def manage_gestures():
    """View and delete uploaded images"""
    gestures = Gesture.query.filter_by(user_id=current_user.id).all()
    return render_template('manage_gestures.html', gestures=gestures)

@app.route('/live_validation')
@login_required
def live_validation():
    """Enhanced validation page with webcam and controls"""
    gestures = Gesture.query.filter_by(user_id=current_user.id).all()
    return render_template('live_validation.html',
                         gestures=gestures,
                         threshold=config.DEFAULT_THRESHOLD)

@app.route('/validation_logs')
@login_required
def validation_logs():
    """View all validation history"""
    logs = ValidationLog.query.filter_by(user_id=current_user.id)\
        .order_by(ValidationLog.timestamp.desc())\
        .limit(500)\
        .all()
    
    correct_count = sum(1 for log in logs if log.is_correct)
    wrong_count = len(logs) - correct_count
    accuracy = round((correct_count / len(logs) * 100), 1) if logs else 0
    
    return render_template('validation_logs.html',
                         logs=logs,
                         correct_count=correct_count,
                         wrong_count=wrong_count,
                         accuracy=accuracy)

# ===========================================
# ENHANCED VALIDATION API ROUTES
# ===========================================

"""
app.py - FIXED API VALIDATION ROUTE
Replace the existing /api/validate route with this improved version
"""

@app.route('/api/validate', methods=['POST'])
@login_required
def api_validate():
    """
    FIXED VALIDATION with debug logging
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        base64_image = data.get('image', '')
        selected_gesture_ids = data.get('gesture_ids', [])
        threshold = float(data.get('threshold', 0.35))  # CHANGED: 0.35 works better
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        print(f"\n🔍 VALIDATION REQUEST ==========================")
        print(f"   Session: {session_id}")
        print(f"   Threshold: {threshold}")
        print(f"   Image data: {'Yes' if base64_image else 'No'}")
        
        if not base64_image:
            print("❌ No image data provided")
            return jsonify({
                'match': False,
                'hand_detected': False,
                'message': 'No image data'
            })
        
        # Process image with MediaPipe
        processor = GestureProcessor()
        live_landmarks = processor.process_base64_image(base64_image)
        
        # If no hand detected
        if live_landmarks is None:
            print("❌ No hand detected in image")
            return jsonify({
                'match': False,
                'hand_detected': False,
                'message': 'No hand detected in frame'
            })
        
        if len(live_landmarks) != 21:
            print(f"❌ Incomplete hand landmarks: {len(live_landmarks)}/21")
            return jsonify({
                'match': False,
                'hand_detected': False,
                'message': 'Incomplete hand detection'
            })
        
        print(f"✅ Hand detected with {len(live_landmarks)} landmarks")
        print(f"   Wrist: x={live_landmarks[0]['x']:.3f}, y={live_landmarks[0]['y']:.3f}")
        print(f"   Index tip: x={live_landmarks[8]['x']:.3f}, y={live_landmarks[8]['y']:.3f}")
        print(f"   Middle tip: x={live_landmarks[12]['x']:.3f}, y={live_landmarks[12]['y']:.3f}")
        
        # Get gestures to validate against
        gestures_dict = {}
        
        if selected_gesture_ids:
            # User selected specific gestures
            print(f"📋 Selected gesture IDs: {selected_gesture_ids}")
            for gesture_id in selected_gesture_ids:
                try:
                    gesture_id_int = int(gesture_id)
                    gesture = Gesture.query.filter_by(
                        id=gesture_id_int,
                        user_id=current_user.id
                    ).first()
                    
                    if gesture and gesture.samples:
                        samples = [sample.landmarks for sample in gesture.samples]
                        gestures_dict[gesture.name] = samples
                        print(f"   ✓ Added: {gesture.name} ({len(samples)} samples)")
                except (ValueError, TypeError) as e:
                    print(f"   ⚠️  Invalid gesture ID {gesture_id}: {e}")
                    continue
        else:
            # Check all user's gestures
            gestures = Gesture.query.filter_by(user_id=current_user.id).all()
            print(f"📋 Using ALL gestures ({len(gestures)} total)")
            for gesture in gestures:
                if gesture and gesture.samples:
                    samples = [sample.landmarks for sample in gesture.samples]
                    gestures_dict[gesture.name] = samples
                    print(f"   ✓ Added: {gesture.name} ({len(samples)} samples)")
        
        if not gestures_dict:
            print("❌ No gestures available to check")
            return jsonify({
                'match': False,
                'hand_detected': True,
                'message': 'No gestures available for validation'
            })
        
        print(f"\n🎯 COMPARING AGAINST {len(gestures_dict)} GESTURES:")
        for gesture_name in gestures_dict.keys():
            print(f"   • {gesture_name}")
        
        # Perform validation using IMPROVED algorithm
        result = validate_against_multiple_gestures(
            live_landmarks,
            gestures_dict,
            threshold
        )
        
        response_data = {
            'hand_detected': True,
            'match': False,
            'session_id': session_id,
            'log_id': None,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        if result:
            gesture_name, distance_val, confidence = result
            
            print(f"\n✅ MATCH FOUND!")
            print(f"   Gesture: {gesture_name}")
            print(f"   Distance: {distance_val:.4f}")
            print(f"   Confidence: {confidence:.1f}%")
            print(f"   Threshold: {threshold}")
            
            # Create validation log
            expected_gestures = list(gestures_dict.keys())
            
            # Consider it correct if confidence is good
            is_correct = confidence > 50.0  # CHANGED: Lower to 50% for better detection
            
            log = ValidationLog(
                user_id=current_user.id,
                detected_gesture=gesture_name,
                expected_gestures=json.dumps(expected_gestures) if expected_gestures else None,
                is_correct=is_correct,
                distance=distance_val,
                threshold_used=threshold,
                session_id=session_id
            )
            
            db.session.add(log)
            db.session.commit()
            
            response_data.update({
                'match': True,
                'gesture_name': gesture_name,
                'distance': float(distance_val),
                'confidence': float(confidence),
                'log_id': log.id,
                'is_correct': is_correct
            })
            
            print(f"   ✓ Log saved (ID: {log.id})")
            
        else:
            # No confident match found
            print(f"\n❌ NO MATCH FOUND")
            print(f"   Threshold: {threshold}")
            print(f"   Available gestures: {list(gestures_dict.keys())}")
            
            expected_gestures = list(gestures_dict.keys())
            
            log = ValidationLog(
                user_id=current_user.id,
                detected_gesture=None,
                expected_gestures=json.dumps(expected_gestures) if expected_gestures else None,
                is_correct=False,
                distance=None,
                threshold_used=threshold,
                session_id=session_id
            )
            
            db.session.add(log)
            db.session.commit()
            
            response_data.update({
                'log_id': log.id,
                'is_correct': False,
                'message': 'Hand detected but no matching gesture found'
            })
            
            print(f"   ✓ Log saved (ID: {log.id})")
        
        print(f"📤 Sending response: match={response_data.get('match', False)}")
        print(f"============================================\n")
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"\n❌ VALIDATION ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"============================================\n")
        
        return jsonify({
            'error': str(e), 
            'success': False,
            'hand_detected': False,
            'match': False
        }), 500

# Also add this helper route for batch saving
# Replace these API routes in app.py

@app.route('/api/save-validation-batch', methods=['POST'])
@login_required
def api_save_validation_batch():
    """
    FIXED: Save only correct results OR all results based on mode
    """
    try:
        data = request.get_json()
        results = data.get('results', [])
        mode = data.get('mode', 'all')  # 'correct' or 'all'
        
        print(f"\n💾 SAVE REQUEST ==========================")
        print(f"   Mode: {mode}")
        print(f"   Total results: {len(results)}")
        
        if not results:
            return jsonify({'error': 'No results to save'}), 400
        
        saved_count = 0
        
        # Filter results based on mode
        if mode == 'correct':
            results_to_keep = [r for r in results if r.get('correct', False)]
            results_to_delete = [r for r in results if not r.get('correct', False)]
        else:
            results_to_keep = results
            results_to_delete = []
        
        print(f"   Keep: {len(results_to_keep)}")
        print(f"   Delete: {len(results_to_delete)}")
        
        # Keep the correct/all results (they're already in DB, just confirm)
        for result in results_to_keep:
            if result.get('log_id'):
                saved_count += 1
        
        # Delete wrong results if mode is 'correct'
        deleted_count = 0
        for result in results_to_delete:
            log_id = result.get('log_id')
            if log_id:
                log = ValidationLog.query.get(log_id)
                if log and log.user_id == current_user.id:
                    db.session.delete(log)
                    deleted_count += 1
        
        db.session.commit()
        
        print(f"   ✅ Saved: {saved_count}, Deleted: {deleted_count}")
        print(f"============================================\n")
        
        return jsonify({
            'success': True,
            'saved_count': saved_count,
            'deleted_count': deleted_count,
            'message': f'Saved {saved_count} validation results'
        })
        
    except Exception as e:
        print(f"❌ Error saving batch: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/discard-validation-batch', methods=['POST'])
@login_required
def api_discard_validation_batch():
    """
    FIXED: Delete ALL validation logs from session
    """
    try:
        data = request.get_json()
        results = data.get('results', [])
        
        print(f"\n🗑️  DISCARD REQUEST ==========================")
        print(f"   Total results to discard: {len(results)}")
        
        if not results:
            return jsonify({'error': 'No results to discard'}), 400
        
        deleted_count = 0
        
        # Delete all logs from this session
        for result in results:
            log_id = result.get('log_id')
            if log_id:
                log = ValidationLog.query.get(log_id)
                if log and log.user_id == current_user.id:
                    db.session.delete(log)
                    deleted_count += 1
        
        db.session.commit()
        
        print(f"   ✅ Deleted: {deleted_count} logs")
        print(f"============================================\n")
        
        return jsonify({
            'success': True,
            'deleted_count': deleted_count,
            'message': f'Discarded {deleted_count} validation results'
        })
        
    except Exception as e:
        print(f"❌ Error discarding batch: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/recent-activity')
@login_required
def api_recent_activity():
    """Get recent validation logs"""
    recent = ValidationLog.query.filter_by(
        user_id=current_user.id
    ).order_by(
        ValidationLog.timestamp.desc()
    ).limit(10).all()
    
    logs_data = []
    for log in recent:
        logs_data.append({
            'id': log.id,
            'detected_gesture': log.detected_gesture,
            'is_correct': log.is_correct,
            'timestamp': log.timestamp.strftime('%H:%M'),
            'distance': log.distance,
            'confidence': round((1 - (log.distance or 0) / (log.threshold_used or 0.35)) * 100, 1) if log.distance else 0
        })
    
    return jsonify(logs_data)

@app.route('/api/test-detection', methods=['POST'])
def test_detection():
    """Simple test endpoint to check if hand detection works"""
    try:
        data = request.get_json()
        base64_image = data.get('image', '')
        
        processor = GestureProcessor()
        landmarks = processor.process_base64_image(base64_image)
        
        if landmarks:
            return jsonify({
                'success': True,
                'hand_detected': True,
                'landmark_count': len(landmarks),
                'landmarks': landmarks[:3]  # First 3 for preview
            })
        else:
            return jsonify({
                'success': False,
                'hand_detected': False,
                'message': 'No hand detected'
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===========================================
# GESTURE MANAGEMENT API ROUTES
# ===========================================

@app.route('/api/delete_sample/<int:sample_id>', methods=['DELETE'])
@login_required
def delete_sample(sample_id):
    """Delete individual sample image"""
    try:
        sample = GestureSample.query.get_or_404(sample_id)
        
        # Security check
        if sample.gesture.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Delete file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], sample.image_path)
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"🗑️ Deleted file: {filepath}")
        
        # Delete from database
        db.session.delete(sample)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Sample deleted successfully'})
    
    except Exception as e:
        print(f"❌ Error deleting sample: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete_gesture/<int:gesture_id>', methods=['DELETE'])
@login_required
def delete_gesture(gesture_id):
    """Delete entire gesture with all samples"""
    try:
        gesture = Gesture.query.get_or_404(gesture_id)
        
        if gesture.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Delete all sample files
        deleted_files = 0
        for sample in gesture.samples:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], sample.image_path)
            if os.path.exists(filepath):
                os.remove(filepath)
                deleted_files += 1
        
        # Delete from database (cascade will handle samples)
        db.session.delete(gesture)
        db.session.commit()
        
        print(f"🗑️ Deleted gesture '{gesture.name}' with {deleted_files} files")
        
        return jsonify({
            'success': True, 
            'message': f'Gesture deleted successfully',
            'deleted_samples': len(gesture.samples)
        })
    
    except Exception as e:
        print(f"❌ Error deleting gesture: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/gestures')
@login_required
def api_gestures():
    """Get all gestures for current user"""
    gestures = Gesture.query.filter_by(user_id=current_user.id).all()
    
    gestures_data = []
    for gesture in gestures:
        gestures_data.append({
            'id': gesture.id,
            'name': gesture.name,
            'description': gesture.description,
            'sample_count': gesture.sample_count,
            'created_at': gesture.created_at.strftime('%Y-%m-%d')
        })
    
    return jsonify(gestures_data)

# ===========================================
# STATIC FILES
# ===========================================

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    """Serve uploaded images"""
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        # Return placeholder if file doesn't exist
        from flask import send_file
        import io
        from PIL import Image, ImageDraw
        
        # Create a simple placeholder image
        img = Image.new('RGB', (200, 200), color=(240, 240, 240))
        d = ImageDraw.Draw(img)
        d.text((50, 80), "Image not found", fill=(100, 100, 100))
        
        img_io = io.BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/jpeg')

# ===========================================
# INITIALIZATION
# ===========================================

def init_db():
    """Initialize database tables"""
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@example.com')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("👤 Created default admin user")
            print("   Username: admin")
            print("   Password: admin123")
        
        print("✅ Database initialized!")

def check_dependencies():
    """Check required packages"""
    try:
        import mediapipe
        import numpy
        import cv2
        print("✅ All dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Install with: pip install mediapipe numpy opencv-python pillow")
        return False

if __name__ == '__main__':
    if check_dependencies():
        init_db()
        print("\n" + "="*70)
        print("🚀 ENHANCED GESTURE VALIDATION SYSTEM")
        print("="*70)
        print("📍 URL: http://127.0.0.1:5000")
        print("✨ Enhanced Features:")
        print("   • Better gesture discrimination")
        print("   • Save/don't save option for each validation")
        print("   • Threshold control (0.1-0.5)")
        print("   • Select specific gestures to validate against")
        print("   • Clean dashboard without duplicate stats")
        print("   • Live webcam with controls")
        print("   • Complete validation history")
        print("   • Gesture and sample management with delete")
        print("="*70 + "\n")
        app.run(debug=True, host='127.0.0.1', port=5000)