import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import math
import time
from collections import deque

# Initialize MediaPipe Hands
hands_detector = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
drawing_utils = mp.solutions.drawing_utils

# Screen dimensions
screen_width, screen_height = pyautogui.size()

# Webcam capture
capture = cv2.VideoCapture(0)

# Buffers and state
trail = []
position_buffer = deque(maxlen=5)
dragging = False
last_click_time = 0
last_right_click_time = 0

# Gesture cooldown in seconds
CLICK_COOLDOWN = 1.0
RIGHT_CLICK_COOLDOWN = 1.0

def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def smooth_position(pos_buffer):
    if not pos_buffer:
        return None
    avg_x = int(sum([p[0] for p in pos_buffer]) / len(pos_buffer))
    avg_y = int(sum([p[1] for p in pos_buffer]) / len(pos_buffer))
    return (avg_x, avg_y)

while True:
    ret, frame = capture.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hands_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    gesture_text = ""

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            points = {}

            for id, lm in enumerate(landmarks):
                x, y = int(lm.x * frame_width), int(lm.y * frame_height)
                points[id] = (x, y)

            index_tip = points[8]
            thumb_tip = points[4]
            middle_tip = points[12]

            # Smooth cursor position
            position_buffer.append(index_tip)
            smoothed_pos = smooth_position(position_buffer)

            if smoothed_pos:
                screen_x = screen_width / frame_width * smoothed_pos[0]
                screen_y = screen_height / frame_height * smoothed_pos[1]
                pyautogui.moveTo(screen_x, screen_y)
                trail.append(smoothed_pos)

            # Drag & Drop
            if distance(index_tip, thumb_tip) < 40:
                if not dragging and (time.time() - last_click_time > CLICK_COOLDOWN):
                    pyautogui.mouseDown()
                    dragging = True
                    last_click_time = time.time()
                gesture_text = "Dragging"
            else:
                if dragging:
                    pyautogui.mouseUp()
                    dragging = False

            # Right Click
            if distance(thumb_tip, middle_tip) < 40:
                if time.time() - last_right_click_time > RIGHT_CLICK_COOLDOWN:
                    pyautogui.rightClick()
                    gesture_text = "Right Click"
                    last_right_click_time = time.time()

            # Scroll
            if distance(index_tip, middle_tip) < 30:
                gesture_text = "Scrolling"
                if len(trail) > 1:
                    dy = trail[-1][1] - trail[-2][1]
                    if abs(dy) > 2:
                        pyautogui.scroll(-int(dy))

            # Draw laser trail
            for i in range(1, len(trail)):
                if trail[i - 1] is None or trail[i] is None:
                    continue
                cv2.line(frame, trail[i - 1], trail[i], (0, 0, 255), 2)

            # Display gesture name
            if gesture_text:
                cv2.putText(frame, f"Gesture: {gesture_text}", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)

    # Limit trail length
    if len(trail) > 50:
        trail = trail[-50:]

    cv2.imshow("🖱️ Virtual Mouse", frame)
    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
