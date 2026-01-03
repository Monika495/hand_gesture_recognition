"""
gesture_processor.py - IMPROVED MediaPipe Hand Detection
FIXED VERSION with better detection parameters
"""
import cv2
import mediapipe as mp
import numpy as np
import base64
import time

class GestureProcessor:
    def __init__(self):
        print("🔄 Initializing GestureProcessor...")
        
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        
        # For static images - USE HIGHER CONFIDENCE
        print("   Creating static hand detector...")
        self.hands_static = self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,  # Only one hand
            min_detection_confidence=0.7,  # HIGHER: 0.7 for better accuracy
            min_tracking_confidence=0.5,
            model_complexity=1  # Balanced model
        )
        
        # For video/webcam - USE BETTER SETTINGS
        print("   Creating video hand detector...")
        self.hands_video = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,  # HIGHER: 0.7
            min_tracking_confidence=0.5,
            model_complexity=1
        )
        
        print("✅ GestureProcessor initialized successfully")
    
    def process_image(self, image_path):
        """
        Extract landmarks from image file
        Returns: List of 21 landmarks as dicts
        """
        print(f"\n📷 Processing image: {image_path}")
        try:
            image = cv2.imread(image_path)
            if image is None:
                print("❌ Failed to load image")
                return None
            
            print(f"   Image size: {image.shape[1]}x{image.shape[0]}")
            
            # Convert BGR to RGB (MediaPipe requires RGB)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Process with MediaPipe
            results = self.hands_static.process(image_rgb)
            
            if not results.multi_hand_landmarks:
                print("❌ No hand detected in static image")
                return None
            
            print(f"✅ Hand detected! Found {len(results.multi_hand_landmarks)} hand(s)")
            
            # Get first hand (assuming single hand)
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Extract landmarks with better formatting
            landmarks = []
            for idx, lm in enumerate(hand_landmarks.landmark):
                landmarks.append({
                    'x': float(lm.x),
                    'y': float(lm.y),
                    'z': float(lm.z)
                })
                
                if idx == 0:  # Wrist
                    print(f"   Wrist: x={lm.x:.3f}, y={lm.y:.3f}, z={lm.z:.3f}")
                elif idx == 8:  # Index finger tip
                    print(f"   Index tip: x={lm.x:.3f}, y={lm.y:.3f}")
            
            print(f"✅ Extracted {len(landmarks)} landmarks")
            return landmarks
            
        except Exception as e:
            print(f"❌ Error processing image: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def process_base64_image(self, base64_image):
        """
        Extract landmarks from base64 webcam image
        Returns: List of 21 landmarks as dicts
        """
        start_time = time.time()
        print(f"\n📹 Processing webcam frame...")
        
        try:
            # Clean base64 string if it has data URL prefix
            if ',' in base64_image:
                base64_image = base64_image.split(',')[1]
                print("   Removed data URL prefix")
            
            # Decode base64 to image
            image_bytes = base64.b64decode(base64_image)
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                print("❌ Failed to decode base64 image")
                return None
            
            print(f"   Decoded image: {image.shape[1]}x{image.shape[0]}")
            
            # Flip image horizontally for mirror effect (like webcam)
            image = cv2.flip(image, 1)
            
            # Convert to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Process with MediaPipe
            results = self.hands_video.process(image_rgb)
            
            if not results.multi_hand_landmarks:
                print("❌ No hand detected in webcam frame")
                return None
            
            print(f"✅ Hand detected! Found {len(results.multi_hand_landmarks)} hand(s)")
            
            # Get first hand
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Extract landmarks
            landmarks = []
            for idx, lm in enumerate(hand_landmarks.landmark):
                landmarks.append({
                    'x': float(lm.x),
                    'y': float(lm.y),
                    'z': float(lm.z)
                })
            
            # Draw landmarks for debugging (optional)
            # self.mp_draw.draw_landmarks(
            #     image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
            #     self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            #     self.mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2)
            # )
            
            # Save debug image (optional)
            # cv2.imwrite('debug_frame.jpg', image)
            
            # Show key points
            if landmarks:
                print(f"   Wrist: x={landmarks[0]['x']:.3f}, y={landmarks[0]['y']:.3f}")
                print(f"   Index tip: x={landmarks[8]['x']:.3f}, y={landmarks[8]['y']:.3f}")
                print(f"   Middle tip: x={landmarks[12]['x']:.3f}, y={landmarks[12]['y']:.3f}")
            
            processing_time = time.time() - start_time
            print(f"✅ Processing complete: {processing_time:.2f}s, {len(landmarks)} landmarks")
            
            return landmarks
            
        except Exception as e:
            print(f"❌ Error processing base64: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def process_frame(self, frame):
        """
        Process a video frame (numpy array)
        Useful for real-time processing
        """
        try:
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Convert to RGB
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process with MediaPipe
            results = self.hands_video.process(image_rgb)
            
            if not results.multi_hand_landmarks:
                return None
            
            # Get first hand
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Extract landmarks
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.append({
                    'x': float(lm.x),
                    'y': float(lm.y),
                    'z': float(lm.z)
                })
            
            # Draw landmarks on frame
            self.mp_draw.draw_landmarks(
                frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                self.mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2)
            )
            
            return landmarks, frame
            
        except Exception as e:
            print(f"Error processing frame: {e}")
            return None, frame
    
    def get_hand_position(self, frame):
        """
        Get basic hand position info (for debugging)
        """
        landmarks, processed_frame = self.process_frame(frame)
        
        if landmarks:
            # Get bounding box of hand
            xs = [lm['x'] for lm in landmarks]
            ys = [lm['y'] for lm in landmarks]
            
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            
            return {
                'landmarks': landmarks,
                'bbox': (min_x, min_y, max_x, max_y),
                'center': ((min_x + max_x) / 2, (min_y + max_y) / 2),
                'frame': processed_frame
            }
        
        return None
    
    def test_detection(self):
        """
        Test function to verify MediaPipe is working
        """
        print("\n🧪 Testing MediaPipe hand detection...")
        
        # Create a simple test image (white background with black hand shape)
        test_image = np.ones((480, 640, 3), dtype=np.uint8) * 255
        
        # Add a simple hand-like shape (circle for palm, lines for fingers)
        center = (320, 240)
        cv2.circle(test_image, center, 50, (0, 0, 0), -1)
        
        # Convert to RGB
        image_rgb = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)
        
        # Process
        results = self.hands_static.process(image_rgb)
        
        if results.multi_hand_landmarks:
            print("✅ MediaPipe is working correctly!")
            return True
        else:
            print("⚠️  MediaPipe didn't detect hand in test image")
            print("   This is normal for synthetic images. Try with a real hand photo.")
            return False
    
    def __del__(self):
        """
        Cleanup resources
        """
        print("\n🧹 Cleaning up GestureProcessor resources...")
        try:
            if hasattr(self, 'hands_static'):
                self.hands_static.close()
            if hasattr(self, 'hands_video'):
                self.hands_video.close()
            print("✅ Resources cleaned up")
        except Exception as e:
            print(f"⚠️  Error during cleanup: {e}")


# ===========================================
# TEST FUNCTION - RUN THIS TO CHECK
# ===========================================
def test_processor():
    """Test the gesture processor"""
    print("\n" + "="*60)
    print("   GESTURE PROCESSOR TEST")
    print("="*60)
    
    # Create processor
    processor = GestureProcessor()
    
    # Test with a sample image if available
    test_image_path = "test_hand.jpg"
    import os
    
    if os.path.exists(test_image_path):
        print(f"\n📸 Testing with image: {test_image_path}")
        landmarks = processor.process_image(test_image_path)
        
        if landmarks:
            print(f"✅ Success! Got {len(landmarks)} landmarks")
            
            # Show first few landmarks
            for i in range(min(5, len(landmarks))):
                lm = landmarks[i]
                print(f"   Point {i}: x={lm['x']:.3f}, y={lm['y']:.3f}, z={lm['z']:.3f}")
        else:
            print("❌ No hand detected in test image")
            print("   Try with a clear photo of a hand")
    else:
        print(f"\n⚠️  Test image not found: {test_image_path}")
        print("   Create a file named 'test_hand.jpg' with a clear hand photo")
    
    # Test basic detection
    processor.test_detection()
    
    print("\n" + "="*60)
    print("   TEST COMPLETE")
    print("="*60)


if __name__ == "__main__":
    # Run test if file is executed directly
    test_processor()