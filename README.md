🚀 AI Hand Gesture Validation System










Real-time AI-powered system that detects, validates, and analyzes hand gestures using computer vision and machine learning techniques.

🚀 Quick Start
 • ✨ Features
 • 🛠️ Tech Stack
 • 📚 Architecture
 • 📊 Working

📖 Overview

The AI Hand Gesture Validation System is a real-time web-based application that uses computer vision and AI to detect hand gestures and validate them against predefined reference gestures.

This system integrates webcam input, AI-based hand tracking, and mathematical comparison techniques to provide instant feedback with confidence scores.

🎯 The Problem

In real-world applications like training, safety validation, and gesture-based systems:

Challenges:

❌ Manual gesture validation is inconsistent

❌ No real-time feedback systems

❌ Requires human supervision

❌ High chances of error

💡 Solution

This project solves the problem by:

✅ Capturing real-time gestures using webcam

✅ Detecting hand landmarks using AI

✅ Comparing gestures with reference data

✅ Providing instant feedback (Correct / Incorrect)

✅ Storing results for analysis

🎯 Why This Project?
Feature	Description
⚡ Real-Time Detection	Instant gesture recognition using webcam
🧠 AI-Based System	Uses MediaPipe for accurate hand tracking
📊 Confidence Score	Provides match percentage
🔔 Feedback System	Sound + visual result
💾 Data Logging	Stores validation history
✨ Key Features
🎥 Real-Time Gesture Detection

Capture live hand gestures using webcam.

🧠 AI-Based Landmark Detection

Detect 21 hand landmarks using MediaPipe.

📏 Smart Comparison Algorithm

Uses Euclidean distance for gesture matching.

📊 Confidence Calculation

Shows how accurate the match is.

🌐 Web Interface

Interactive UI built using Flask.

🔗 Public Access

Share your app using ngrok.

🛠️ Technology Stack
🔹 Backend

Python 3.10 → Core logic

Flask → Web server

🔹 Computer Vision

OpenCV → Webcam capture

MediaPipe → AI hand detection

🔹 Database

SQLite → Store logs

🔹 Frontend

HTML, CSS, JS → UI

🔹 Deployment

ngrok → Public link

📚 System Architecture
User → Frontend → Flask → OpenCV → RGB Conversion → MediaPipe
→ Landmark Extraction → Comparison → Result → SQLite → Response
🔄 Working Process
Step 1: Capture Frame

OpenCV captures webcam frame.

Step 2: Convert Image

Convert BGR → RGB for AI model.

rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
Step 3: Detect Hand

MediaPipe detects:

21 landmarks (x, y, z)

Step 4: Compare Gestures

Using Euclidean Distance:

distance = √((x1-x2)² + (y1-y2)² + (z1-z2)²)
Step 5: Decision
If distance < threshold → MATCH ✅
Else → NOT MATCH ❌
Step 6: Store Result

Saved in SQLite database.

📊 Database Structure

Table: logs

Field	Description
id	Unique ID
gesture	Gesture name
result	Match / No Match
confidence	%
timestamp	Time
📦 Installation
Step 1: Clone Repo
git clone https://github.com/Monika495/hand_gesture_recognition.git
cd gesture-validation-webapp
Step 2: Create Virtual Environment
python -m venv venv
venv\Scripts\activate
Step 3: Install Dependencies
pip install mediapipe==0.10.8 opencv-python numpy flask
Step 4: Run App
python app.py

👉 Open:

http://127.0.0.1:5000
🌐 Public Deployment (ngrok)
ngrok http 5000

👉 Example:

https://xxxxx.ngrok-free.dev
📁 Project Structure
gesture-validation-webapp/
│
├── app.py
├── database.db
├── gesture_processor.py
│
├── templates/
├── static/
│
└── venv/
🚀 Use Cases

🏭 Industrial safety training

✋ Sign language systems

🎮 Gesture-based control

🧑‍🏫 Education

🚧 Challenges Faced

MediaPipe version compatibility

Real-time processing speed

Gesture accuracy tuning

🔮 Future Scope

Deep learning gesture classification

Multi-hand detection

Cloud deployment

👨‍💻 Developer

Monika P
AI & Computer Vision Enthusiast

<div align="center">
⭐ Star this repo if you like it!

Made with ❤️ by Monika P

</div>
