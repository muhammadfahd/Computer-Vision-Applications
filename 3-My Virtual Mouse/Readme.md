# Virtual Mouse with Hand Gesture Recognition 🤚🖱️

A Python-based **Virtual Mouse** application that allows you to control the cursor on your screen using hand gestures captured through your webcam. The app uses **MediaPipe** for hand tracking, **PyAutoGUI** for mouse control, and **OpenCV** for image processing. It supports gestures like clicking, dragging, scrolling, and more.

---

## Features ✨

- **🖱️ Virtual Mouse**: Move the cursor using your hand movements.
- **✅ Drag & Drop**: Pinch gesture to click and hold, release to drop.
- **🖱️ Right Click**: Gesture recognition with thumb + middle finger touch.
- **🔄 Scroll**: Vertical hand movement for scrolling up/down.
- **👀 Gesture Display**: On-screen feedback to show the detected gesture.
- **🔴 Hand Trail**: Visual trail following your finger for precision.
- **🚀 Gesture Smoothing**: Reduced cursor jitter for smoother movement.
- **🔒 Gesture Cooldown**: Cooldown added for actions like clicks and right-clicks to prevent accidental repeats.

---

## Demo Picture 🎥

![alt text](<Screenshot 2025-04-18 113957.png>)

---

## Requirements ⚙️

Make sure to install the necessary dependencies:

```bash
pip install opencv-python mediapipe pyautogui numpy

```

## How It Works 🔧
- Hand Tracking: MediaPipe’s hand tracking module is used to detect key landmarks on the hand, specifically the index and thumb.

- Cursor Control: We map the positions of the detected hand landmarks to the screen's resolution to simulate mouse movement.

- Gestures:

  - Clicking: Triggered by pinching the thumb and index finger.

  - Right Click: Triggered by touching the thumb and middle finger.

  - Scrolling: Detected when fingers move vertically while in close proximity.

