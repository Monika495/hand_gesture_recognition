"""
validator.py - SIMPLIFIED and ACCURATE gesture validation
"""
import math
import numpy as np
import json

def distance(p1, p2):
    """Calculate 3D Euclidean distance"""
    return math.sqrt(
        (p1['x'] - p2['x'])**2 +
        (p1['y'] - p2['y'])**2 +
        (p1['z'] - p2['z'])**2
    )

def normalize_simple(landmarks):
    """
    Simple normalization to wrist point
    """
    if len(landmarks) != 21:
        return None
    
    wrist = landmarks[0]
    normalized = []
    
    for lm in landmarks:
        normalized.append({
            'x': lm['x'] - wrist['x'],
            'y': lm['y'] - wrist['y'],
            'z': lm['z'] - wrist['z']
        })
    
    return normalized

def compare_gestures_simple(live_landmarks, ref_landmarks, threshold=0.35):
    """
    SIMPLIFIED and ACCURATE comparison
    Uses only key points and normalized distances
    """
    if live_landmarks is None or ref_landmarks is None:
        return (False, float('inf'), 0.0)
    
    if len(live_landmarks) != 21 or len(ref_landmarks) != 21:
        return (False, float('inf'), 0.0)
    
    # 1. Normalize both sets to wrist point
    live_norm = normalize_simple(live_landmarks)
    ref_norm = normalize_simple(ref_landmarks)
    
    if live_norm is None or ref_norm is None:
        return (False, float('inf'), 0.0)
    
    # 2. Calculate distances for KEY POINTS ONLY (fingertips + wrist)
    key_points = [0, 4, 8, 12, 16, 20]  # wrist + all fingertips
    
    distances = []
    for idx in key_points:
        dist = math.sqrt(
            (live_norm[idx]['x'] - ref_norm[idx]['x'])**2 +
            (live_norm[idx]['y'] - ref_norm[idx]['y'])**2 +
            (live_norm[idx]['z'] - ref_norm[idx]['z'])**2
        )
        distances.append(dist)
    
    avg_distance = sum(distances) / len(distances)
    
    # 3. Calculate confidence (0-100)
    confidence = max(0.0, 100.0 * (1.0 - (avg_distance / threshold)))
    
    # 4. Check if match
    is_match = avg_distance < threshold and confidence > 40.0
    
    # Debug output
    if is_match:
        print(f"   ✓ Match found: dist={avg_distance:.3f}, conf={confidence:.1f}%")
    else:
        print(f"   ✗ No match: dist={avg_distance:.3f}, conf={confidence:.1f}%")
    
    return (is_match, avg_distance, confidence)

def validate_against_multiple_gestures(live_landmarks, gestures_dict, threshold=0.35):
    """
    Validate against multiple gestures, return BEST match
    Uses simple comparison for better accuracy
    """
    if not gestures_dict or live_landmarks is None:
        print("   ⚠️ No gestures to compare or no landmarks")
        return None
    
    if len(live_landmarks) != 21:
        print(f"   ⚠️ Invalid landmarks count: {len(live_landmarks)}/21")
        return None
    
    best_match = None
    best_distance = float('inf')
    best_confidence = 0.0
    
    print(f"   Comparing with {len(gestures_dict)} gestures...")
    
    # Check each gesture
    for gesture_name, ref_samples in gestures_dict.items():
        # Check each sample of this gesture
        for ref_landmarks in ref_samples:
            is_match, dist_val, conf = compare_gestures_simple(
                live_landmarks, 
                ref_landmarks, 
                threshold
            )
            
            # Keep track of best match (even if not matching)
            if dist_val < best_distance:
                best_distance = dist_val
                best_confidence = conf
                if is_match:
                    best_match = gesture_name
    
    print(f"   Best result: gesture='{best_match}', dist={best_distance:.3f}, conf={best_confidence:.1f}%")
    
    # Return match if confidence is good
    if best_match and best_confidence > 50.0:
        return (best_match, best_distance, best_confidence)
    
    return None

# ===========================================
# Alternative comparison methods
# ===========================================

def compare_gestures_angle_based(live_landmarks, ref_landmarks, threshold=0.5):
    """
    Compare gestures using finger angles
    """
    if live_landmarks is None or ref_landmarks is None:
        return (False, float('inf'), 0.0)
    
    # Calculate finger vectors
    finger_tips = [4, 8, 12, 16, 20]  # All fingertips
    finger_mcp = [2, 6, 10, 14, 18]   # Finger bases
    
    angle_diffs = []
    
    for tip_idx, base_idx in zip(finger_tips, finger_mcp):
        # Live vector
        live_vec = [
            live_landmarks[tip_idx]['x'] - live_landmarks[base_idx]['x'],
            live_landmarks[tip_idx]['y'] - live_landmarks[base_idx]['y']
        ]
        
        # Reference vector
        ref_vec = [
            ref_landmarks[tip_idx]['x'] - ref_landmarks[base_idx]['x'],
            ref_landmarks[tip_idx]['y'] - ref_landmarks[base_idx]['y']
        ]
        
        # Calculate angle difference
        live_mag = math.sqrt(live_vec[0]**2 + live_vec[1]**2)
        ref_mag = math.sqrt(ref_vec[0]**2 + ref_vec[1]**2)
        
        if live_mag > 0.001 and ref_mag > 0.001:
            dot = live_vec[0]*ref_vec[0] + live_vec[1]*ref_vec[1]
            cos_angle = dot / (live_mag * ref_mag)
            cos_angle = max(-1.0, min(1.0, cos_angle))
            angle_diff = math.acos(cos_angle) / math.pi  # Normalize to 0-1
            angle_diffs.append(angle_diff)
    
    if not angle_diffs:
        return (False, float('inf'), 0.0)
    
    avg_angle_diff = sum(angle_diffs) / len(angle_diffs)
    confidence = max(0.0, 100.0 * (1.0 - (avg_angle_diff / threshold)))
    is_match = avg_angle_diff < threshold and confidence > 50.0
    
    return (is_match, avg_angle_diff, confidence)

def compare_gestures_hybrid(live_landmarks, ref_landmarks, threshold=0.4):
    """
    Hybrid comparison using both distances and angles
    """
    # Get distance-based comparison
    dist_match, dist_val, dist_conf = compare_gestures_simple(live_landmarks, ref_landmarks, threshold)
    
    # Get angle-based comparison
    angle_match, angle_val, angle_conf = compare_gestures_angle_based(live_landmarks, ref_landmarks, threshold)
    
    # Combine results (weighted average)
    combined_dist = (dist_val * 0.7) + (angle_val * 0.3)
    combined_conf = (dist_conf * 0.7) + (angle_conf * 0.3)
    
    is_match = combined_dist < threshold and combined_conf > 45.0
    
    return (is_match, combined_dist, combined_conf)

# ===========================================
# Utility functions
# ===========================================

def landmarks_to_json(landmarks):
    """Convert landmarks to JSON string"""
    return json.dumps(landmarks)

def json_to_landmarks(json_str):
    """Convert JSON string to landmarks"""
    try:
        return json.loads(json_str)
    except:
        return None

def calculate_hand_size(landmarks):
    """Calculate the size of the hand (for scaling)"""
    if len(landmarks) != 21:
        return 0.0
    
    # Use distance from wrist to middle finger tip
    wrist = landmarks[0]
    middle_tip = landmarks[12]
    
    return distance(wrist, middle_tip)

def get_hand_bounding_box(landmarks):
    """Get bounding box of hand"""
    xs = [lm['x'] for lm in landmarks]
    ys = [lm['y'] for lm in landmarks]
    
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    return {
        'min_x': min_x,
        'min_y': min_y,
        'max_x': max_x,
        'max_y': max_y,
        'width': max_x - min_x,
        'height': max_y - min_y,
        'center_x': (min_x + max_x) / 2,
        'center_y': (min_y + max_y) / 2
    }

# ===========================================
# Test function
# ===========================================

def test_validator():
    """Test the validator functions"""
    print("\n🧪 Testing validator...")
    
    # Create sample landmarks
    sample_landmarks = []
    for i in range(21):
        sample_landmarks.append({
            'x': i * 0.01,
            'y': i * 0.01,
            'z': i * 0.001
        })
    
    # Test normalization
    normalized = normalize_simple(sample_landmarks)
    print(f"✅ Normalization: {len(normalized) if normalized else 0} points")
    
    # Test distance
    p1 = {'x': 0, 'y': 0, 'z': 0}
    p2 = {'x': 1, 'y': 0, 'z': 0}
    dist = distance(p1, p2)
    print(f"✅ Distance calculation: {dist:.2f} (expected: 1.0)")
    
    # Test comparison with same landmarks
    match, dist_val, conf = compare_gestures_simple(sample_landmarks, sample_landmarks, 0.35)
    print(f"✅ Self-comparison: match={match}, dist={dist_val:.3f}, conf={conf:.1f}%")
    
    # Test hand size
    size = calculate_hand_size(sample_landmarks)
    print(f"✅ Hand size: {size:.3f}")
    
    # Test bounding box
    bbox = get_hand_bounding_box(sample_landmarks)
    print(f"✅ Bounding box: {bbox}")
    
    print("\n✅ Validator test complete!")

if __name__ == "__main__":
    test_validator()