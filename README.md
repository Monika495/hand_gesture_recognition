📌 AI-Based Hand Gesture Validation System
🚀 Overview

This project is a real-time hand gesture validation web application that uses computer vision and a pre-trained AI model to detect and verify hand gestures through a webcam. The system compares live hand gestures with predefined reference gestures and provides instant feedback indicating whether the gesture is correct or not.

The application is built using a combination of backend, frontend, and computer vision technologies, and includes logging functionality for analysis.

🎯 Problem Statement

In many domains such as industrial training, safety procedures, and gesture-based communication, there is no automated mechanism to validate whether a user is performing the correct hand gesture. This leads to inefficiencies, lack of standardization, and potential errors.

💡 Solution

This system provides an automated solution by:

Capturing real-time hand gestures using a webcam

Detecting hand landmarks using an AI-based model

Comparing gestures with stored references

Providing instant feedback (Correct / Incorrect)

Logging validation results for analysis

🧠 System Architecture
User → Frontend → Flask Backend → Image Processing → AI Model → Comparison Logic → Database → Response → Frontend
⚙️ Technologies Used
🔹 Python

Used as the core programming language for backend development and integration of all components.

🔹 Flask (Web Framework)

Flask is used to build the backend server and handle communication between the frontend and backend.

Responsibilities:

Handle API requests (e.g., /api/validate)

Process gesture validation logic

Communicate with the database

Send responses to the frontend

🔹 OpenCV (Computer Vision Library)

Used for real-time image capture and preprocessing.

Why OpenCV?

Provides easy access to webcam

Efficient frame capture

Supports image manipulation

Usage:

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
🔹 MediaPipe (AI Hand Tracking Model)

MediaPipe is a pre-trained machine learning framework used for detecting hand landmarks.

Key Functionality:

Detects hand in an image

Extracts 21 landmark points (x, y, z coordinates)

Why MediaPipe?

No need to train a model

High accuracy and real-time performance

Lightweight and efficient

🔹 RGB Conversion (Important Step)

OpenCV captures images in BGR format, while MediaPipe expects RGB format.

Conversion:

rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

Reason:
Ensures correct color representation and improves detection accuracy.

🔹 SQLite (Database)

SQLite is a lightweight, file-based database used to store validation logs.

Why SQLite?

No server setup required

Easy integration with Python (sqlite3)

Suitable for small to medium applications

Data Stored:

Gesture name

Validation result

Confidence score

Timestamp

🔹 Frontend (HTML, CSS, JavaScript)

Used to build the user interface.

Responsibilities:

Capture user interaction

Display validation results

Show dashboard and logs

Play feedback sounds

🔹 ngrok (Tunneling Tool)

Used to expose the locally running Flask application to the public internet.

Purpose:

Generate temporary public URL

Enable remote access for demo/testing

🔄 Working Process (Step-by-Step)

The webcam captures real-time video using OpenCV

The captured frame is converted from BGR to RGB

The RGB image is passed to MediaPipe

MediaPipe detects the hand and extracts 21 landmarks

Landmark data is structured into a coordinate list

The system compares live landmarks with stored reference gestures

Euclidean distance is calculated between corresponding points

The average distance is compared with a threshold value

If distance < threshold → Gesture is Correct

Else → Gesture is Incorrect

Result is stored in SQLite database

Flask sends response to frontend

Frontend displays result and feedback

📐 Gesture Comparison Logic
🔹 Euclidean Distance Formula
distance = √((x1 - x2)² + (y1 - y2)² + (z1 - z2)²)
🔹 Process

Calculate distance for all 21 points

Compute average distance

Compare with threshold

🔹 Decision Rule
If distance < threshold → Match
Else → No Match
📊 Confidence Score

Confidence is inversely proportional to distance:

Lower distance → Higher confidence

Higher distance → Lower confidence

🗄️ Database Design (SQLite)

Table: logs

Column	Description
id	Unique ID
gesture	Gesture name
result	Correct / Incorrect
confidence	Match percentage
timestamp	Time of validation
✨ Features

Real-time gesture validation

Confidence score calculation

Adjustable threshold

Multiple gesture support

Validation logging

Dashboard view

Sound feedback

📦 Installation & Setup
# Clone repository
git clone <your-repo-link>

# Navigate to project
cd gesture-validation-webapp

# Create virtual environment
python -m venv venv

# Activate environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
🌐 Public Access (ngrok)
ngrok http 5000
🎯 Use Cases

Industrial training systems

Safety compliance verification

Gesture-based control systems

Sign language learning

🚧 Limitations

Sensitive to lighting conditions

Limited gesture dataset

Single-hand detection

🔮 Future Enhancements

Deep learning-based gesture classification

Multi-hand support

Mobile application integration

Cloud deployment

🧩 Skills Gained

Backend development using Flask

Computer vision fundamentals

Real-time system design

Database integration (SQLite)

API development

Debugging and deployment

🧠 Key Learning

This project demonstrates how pre-trained AI models can be integrated into real-time applications without requiring custom model training, and how multiple technologies can be combined to build a complete end-to-end system.
