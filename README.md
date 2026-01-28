Fruit Ninja – Hand Gesture Game

**Description**

- The Fruit Ninja Hand Gesture Game is an interactive computer-vision project built using Python, OpenCV, and MediaPipe.  
- It allows users to slice falling fruits in real time using hand gestures captured through a webcam.
- This project demonstrates real-time hand tracking, gesture recognition, and interactive game logic using computer vision techniques.

---

## **Features**
- Slice fruits using hand gestures
- Real-time hand tracking using MediaPipe
- Neon sword / slash visual effect
- Fruit split animation on slicing
- Bomb detection with game-over logic
- Live score tracking
- Works with a standard webcam

---

## **Tech Stack**
- **Python** – Core programming language
- **OpenCV** – Image processing and rendering
- **MediaPipe** – Hand landmark detection
- **NumPy** – Numerical operations

---

## **How to Use**
- Create and activate a virtual environment
- Install required dependencies
- Run the Python script
- Use your hand in front of the webcam to slice fruits
- Avoid bombs to keep the game running

---

## **Setup & Run**

**Create and activate virtual environment**
```bash
python -m venv venv
venv\Scripts\activate

---

Install dependencies

pip install opencv-python mediapipe numpy

---

Run the game

python hand_tracking.py

---

Requirements
- Webcam must be connected
- assets/ folder must be present
- Python version 3.10 or higher

---

Project Structure

fruit-ninja-opencv/
├── assets/
│   ├── apple.png
│   ├── banana.png
│   ├── orange.png
│   └── bomb.png
├── hand_tracking.py
├── webcam_test.py
├── .gitignore
└── README.md

---

Inspiration & Credits 

- Inspired by Fruit Ninja–style gesture-based games and computer-vision demos
- Implementation and logic were developed as a learning exercise with guidance and reference support

---

Disclaimer

- This project is created for educational purposes only
- It is not affiliated with or endorsed by the official Fruit Ninja game 

---

Author
Prarthana Bharathiraja