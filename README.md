# 🔱 Project Sudarshan

Project Sudarshan is a real-time computer vision prototype inspired by the **Sudarshan Chakra of Bhagwan Vishnu**, a symbol of precision, control, and balance.

This project was built as a learning-focused exploration into how real-time vision systems behave in the real world — beyond clean demos and tutorials — and how to design them to feel stable, intentional, and reliable.

---

## 🧠 Project Overview

Project Sudarshan uses **hand gesture recognition** to manifest a rotating chakra anchored to the user’s fingertip in real time.

Although the visual output appears simple, the system behind it required careful handling of instability, noise, and gesture ambiguity that naturally occur in live camera input.

The project prioritizes:
- temporal consistency over single-frame accuracy  
- robustness over quick hacks  
- understanding concepts instead of copying solutions  

---

## ✨ Features

- Real-time hand tracking using MediaPipe
- Gesture-based activation (intent-driven, not accidental)
- Temporal smoothing to reduce landmark jitter
- Stable fingertip anchoring with directional offset
- Transparent AR-style visual overlay using OpenCV
- Modular and maintainable project structure

---

## 🛠️ Tech Stack

- **Python**
- **OpenCV**
- **MediaPipe (Hand Landmarker – `.task` model)**
- **NumPy**

---

## 📂 Project Structure

