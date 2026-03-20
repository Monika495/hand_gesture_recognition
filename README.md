# ✋ Hand Gesture Validation System

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)]()
[![Flask](https://img.shields.io/badge/Flask-WebApp-green.svg)]()
[![OpenCV](https://img.shields.io/badge/OpenCV-ComputerVision-red.svg)]()
[![MediaPipe](https://img.shields.io/badge/MediaPipe-HandTracking-orange.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)]()

> 🚀 A real-time AI-powered hand gesture validation web application that detects and validates user gestures using webcam input.

---

## 📖 Overview

The **Hand Gesture Validation System** is a web-based application that captures live webcam input, detects hand landmarks using AI, and compares gestures with stored references to determine correctness.  

It provides **real-time feedback**, confidence scores, and validation logs through an interactive dashboard.

---

## 🎯 Problem Statement

- Manual gesture validation is difficult and inconsistent.  
- No real-time feedback for gesture-based systems.  
- Lack of simple AI-based validation tools for beginners.  

---

## 💡 Solution

This project solves the problem by:

- Using **AI-based hand tracking**  
- Comparing gestures using **landmark distance calculation**  
- Providing **instant validation (Correct / Wrong)**  
- Storing results in a **database for analysis**  

---

## ✨ Features

- 📷 Live webcam gesture detection  
- 🤖 AI-based hand landmark extraction  
- 🎯 Gesture comparison & validation  
- 📊 Confidence score display  
- 🔊 Beep sound feedback  
- 🧾 Validation logs dashboard  
- ⚙️ Adjustable threshold  

---

## 🛠️ Technology Stack

### 🔹 Backend
- **Python** – Core programming language  
- **Flask** – Web framework  

### 🔹 AI & Computer Vision
- **MediaPipe** – Detects 21 hand landmarks using pre-trained ML model  
- **OpenCV** – Captures webcam frames and processes images  

### 🔹 Frontend
- **HTML, CSS, JavaScript** – User interface  

### 🔹 Database
- **SQLite3** – Stores gesture data and validation logs  

### 🔹 Deployment
- **Ngrok** – Exposes local server to public internet  

---

## ⚙️ How It Works

1. Webcam captures live video using OpenCV  
2. Frame is converted from **BGR → RGB**  
3. MediaPipe detects **21 hand landmarks**  
4. Landmarks are compared with stored gesture data  
5. Distance is calculated between points  
6. If distance < threshold → ✅ Match  
7. Result is sent to frontend and displayed  

---

## 📐 Gesture Matching Logic

- Each hand has **21 landmarks (x, y coordinates)**  
- Distance is calculated using:  

\[
\text{Distance} = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}
\]

- Lower distance = better match  
- Confidence is calculated based on distance  

---

## 📦 Installation

### 🔹 Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/hand_gesture_recognition.git
cd hand_gesture_recognition
🔹 Step 2: Create Virtual Environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
🔹 Step 3: Install Dependencies
pip install -r requirements.txt
🔹 Step 4: Run Application
python app.py

Open browser: http://127.0.0.1:5000

🔹 Step 5: Public Access via Ngrok
ngrok http 5000

You will get a public link like: https://xxxxx.ngrok-free.app

🗄️ Database (SQLite3)

Automatically created when app runs

Stores:

Gesture samples

Validation logs

Example Table Structure:
| id | gesture_name | confidence | timestamp |

📊 Project Structure
gesture-validation-webapp/
│
├── app.py
├── requirements.txt
├── database.db
│
├── static/
│   ├── css/
│   ├── js/
│
├── templates/
│   ├── index.html
│   ├── dashboard.html
│
└── README.md
🚀 Future Scope

Multi-hand gesture support

Deep learning model for better accuracy

Mobile support

Cloud deployment (AWS / Render)

Gesture-based authentication system

💼 Skills Gained

Computer Vision

AI Model Integration

Flask Web Development

Database Handling (SQLite)

API Development

Real-time System Design

👨‍💻 Developer

Monika P
CSE Student | AI & Web Development Enthusiast
