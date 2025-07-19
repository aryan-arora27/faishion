# 👗 Faishion - AI-Powered Outfit Recommendation App

fAIshion is a full-stack Flutter application that uses **YOLO-based object detection** and an **AI-powered recommendation engine** to analyze uploaded outfit images and suggest optimal clothing color combinations based on the user's **skin tone**. Designed to work responsively across devices, the app integrates **machine learning**, **computer vision**, and **RESTful APIs** to deliver personalized fashion advice.

---

## 🚀 Features

- 🔍 **YOLOv8 Object Detection** to identify outfit types from uploaded images (e.g., shirt, pants).
- 🎨 **Color Combination Recommender** trained on curated datasets to suggest combinations that suit different skin tones.
- 👤 **User Authentication** with skin tone selection stored in the backend.
- 🕒 **Outfit History Tracking** with timestamped uploads and AI suggestions.
- 📷 **In-app Camera/Upload** functionality using `image_picker` for quick outfit capture.

---

## 🧠 Tech Stack

### 🧠 Machine Learning / AI
- **YOLOv8** for apparel detection (trained on labeled outfit datasets).
- **Scikit-learn / Pandas** for outfit color recommendation logic based on extracted outfit features and skin tone.

### 🖥️ Backend (Python)
- **Flask** as the REST API framework
- **SQLAlchemy + SQLite** for user and history data storage
- **Flask-CORS** for secure communication between backend and frontend

### 📱 Frontend (Flutter)
- **Flutter & Dart** for cross-platform mobile UI
- **image_picker** for photo selection and capture
- **http** package for backend communication
- **Responsive UI** that works well on phones and tablets

