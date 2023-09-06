import cv2
import numpy as np

def nothing(x):
    pass

# Initializing video capture object
capture = cv2.VideoCapture(0)
cv2.namedWindow('live_sketch')

# Creating trackbars
cv2.createTrackbar('lower', 'live_sketch', 0, 255, nothing)
cv2.createTrackbar('Upper', 'live_sketch', 0, 255, nothing)


while True:
    ret, frame = capture.read()
    if not ret:
        break

    # Get trackbar values
    lower = cv2.getTrackbarPos('lower', 'live_sketch')
    upper = cv2.getTrackbarPos('Upper', 'live_sketch')

  
    # 1. Convert to gray, add Gaussian blur, then apply Canny edge detection and thresholding
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (7, 7), 0)
    image = cv2.Canny(image, lower, upper)
    ret, image = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY_INV)

   



    # Display original video
    cv2.imshow('Original Video', frame)
    # Display sketch
    cv2.imshow('live_sketch', image)

    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
