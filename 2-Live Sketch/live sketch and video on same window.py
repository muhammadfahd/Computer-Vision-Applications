import cv2
import numpy as np

# Initializing video capture object
capture = cv2.VideoCapture(0)

while True:
    ret, im = capture.read()
    roi=cv2.selectROI("original",im,False,False)
    cv2.destroyAllWindows()
    break

while True:
    ret, frame = capture.read()
    if not ret:
        break

    # For sketch effect
    selected_roi = frame[int(roi[1]):int(roi[1]+roi[3]),
                          int(roi[0]):int(roi[0]+roi[2])]

    # 1. Convert to gray, add Gaussian blur, then apply Canny edge detection and thresholding
    selected_roi_gray = cv2.cvtColor(selected_roi, cv2.COLOR_BGR2GRAY)
    selected_roi_blur = cv2.GaussianBlur(selected_roi_gray, (7, 7), 0)
    selected_roi_canny = cv2.Canny(selected_roi_blur, 12, 55)
    _, selected_roi_thresh = cv2.threshold(selected_roi_canny, 50, 255, cv2.THRESH_BINARY_INV)

    selected_roi_color = cv2.cvtColor(selected_roi_thresh, cv2.COLOR_GRAY2BGR)
    frame[int(roi[1]):int(roi[1]+roi[3]),
          int(roi[0]):int(roi[0]+roi[2])] = selected_roi_color

    # Display original video
    cv2.imshow('Original Video', frame)

    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
