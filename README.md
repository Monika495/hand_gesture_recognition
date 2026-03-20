🚀 AI Hand Gesture Validation System

Python 3.10 | Flask | MediaPipe | OpenCV | SQLite | Computer Vision

Real-time AI-powered system to detect, validate, and analyze hand gestures using webcam input and intelligent comparison algorithms.

🚀 Quick Links

📖 Overview • 🎯 Problem • 💡 Solution • ✨ Features • 🛠️ Tech Stack • ⚙️ Setup • 📊 Working • 📁 Structure • 🚀 Deployment

📖 Overview

This project is a real-time AI-based hand gesture validation web application that captures hand gestures through a webcam, detects hand landmarks using a pre-trained AI model, and validates them against stored reference gestures.

The system provides:

Instant feedback (Correct / Incorrect)

Confidence score

Gesture comparison analysis

Validation logs and dashboard

🎯 The Problem

Many real-world scenarios require accurate gesture validation, such as:

Industrial safety procedures

Training environments

Gesture-based systems

Sign language learning

Challenges:

❌ Manual validation is inconsistent

❌ No automation for gesture checking

❌ Requires human supervision

❌ Error-prone and inefficient

💡 The Solution

This system automates gesture validation using AI:

✅ Captures live hand gestures
✅ Detects hand landmarks using AI
✅ Compares with reference gestures
✅ Provides real-time feedback
✅ Stores validation results

✨ Key Features

🎥 Real-time webcam gesture detection

🧠 AI-based hand landmark extraction

📏 Distance-based gesture comparison

📊 Confidence score calculation

🔔 Sound feedback (beep for result)

🗂️ Gesture management system

📈 Validation logs & dashboard

🌐 Public access using tunneling

🛠️ Technology Stack
🔹 Backend

Python 3.10 → Core programming

Flask → Web server & API handling

🔹 Computer Vision

OpenCV → Webcam capture & image processing

MediaPipe → AI hand landmark detection

🔹 Database

SQLite → Store gesture logs & results

🔹 Frontend

HTML, CSS, JavaScript → UI & interaction

🔹 Deployment

ngrok → Public URL tunneling

⚙️ Installation & Setup
Step 1: Clone Repository
git clone https://github.com/Monika495/hand_gesture_recognition.git
cd gesture-validation-webapp
Step 2: Create Virtual Environment
python -m venv venv
venv\Scripts\activate
Step 3: Install Dependencies
pip install --upgrade pip
pip install mediapipe==0.10.8 opencv-python numpy flask
Step 4: Run the Application
python app.py

👉 Open browser:

http://127.0.0.1:5000
🌐 Public Access (ngrok)
ngrok http 5000

👉 You will get:

https://xxxx.ngrok-free.dev
🔄 Working Process
Step-by-Step Flow
Webcam → OpenCV → BGR → RGB → MediaPipe → Landmarks
→ Comparison → Distance → Threshold → Result
→ Database → Frontend Display
🧠 Core Logic (Gesture Comparison)
🔹 Landmark Detection

MediaPipe detects:

21 hand landmarks (x, y, z)
🔹 RGB Conversion

OpenCV gives:

BGR format

Converted to:

RGB format
rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
🔹 Distance Calculation

Euclidean Distance:

distance = √((x1 - x2)² + (y1 - y2)² + (z1 - z2)²)
🔹 Matching Logic
If distance < threshold → MATCH ✅
Else → NOT MATCH ❌
🔹 Confidence

Lower distance → Higher confidence

Higher distance → Lower confidence

📊 Database (SQLite)
Table: logs
Field	Description
id	Unique ID
gesture	Gesture name
result	Match / No Match
confidence	Percentage
timestamp	Time
📁 Project Structure
gesture-validation-webapp/
│
├── app.py
├── gesture_processor.py
├── database.db
│
├── templates/
│   ├── index.html
│   ├── dashboard.html
│
├── static/
│   ├── css/
│   ├── js/
│
└── venv/
🚀 Use Cases

🏭 Industrial training validation

✋ Sign language systems

🎮 Gesture-based control

🧑‍🏫 Educational tools

🚧 Challenges Faced

MediaPipe compatibility issues (Python version)

Real-time processing optimization

Gesture accuracy tuning

Threshold selection

🔮 Future Improvements

Deep learning-based gesture classification

Multi-hand support

Mobile/web deployment

Cloud hosting

🧠 Skills Gained

Computer Vision (OpenCV, MediaPipe)

Backend Development (Flask)

Database Integration (SQLite)

Real-time system design

Debugging & deployment

👨‍💻 Developer

Monika P
AI & Computer Vision Enthusiast

⭐ Summary

This project demonstrates how AI, computer vision, and web technologies can be combined to build a real-time gesture validation system that is efficient, scalable, and practical for real-world applications.

❤️ Final Note

⭐ If you found this project useful, consider starring the repository!
