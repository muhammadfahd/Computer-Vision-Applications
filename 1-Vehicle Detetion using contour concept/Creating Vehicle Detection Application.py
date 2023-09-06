import cv2
import numpy as np

kernel = None
# Loading the video
cap = cv2.VideoCapture('media/videos/carsvid.mp4')

# Initialize the background object
background_object = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

while True:
    # Reading frame by frame
    ret, frame = cap.read()
    if not ret:
        break

    # Apply the background object on frame to get the mask
    fgmask = background_object.apply(frame)

    # Performing threshold for removing shadows
    _, fgmask = cv2.threshold(fgmask, 250, 255, cv2.THRESH_BINARY)

    # Applying morphological operations
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    fgmask = cv2.dilate(fgmask, kernel, iterations=2)

    # Detecting contours
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    copied_frame = frame.copy()

    for cnt in contours:
        if cv2.contourArea(cnt) > 400:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(copied_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(copied_frame, "Car detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1,
                        cv2.LINE_AA)
            
         

    forgroundPart = cv2.bitwise_and(frame, frame, mask=fgmask)
    stack = np.hstack((frame, forgroundPart, copied_frame))

   


    cv2.imshow("Application", cv2.resize(stack, None, fx=0.5, fy=0.5))

    k = cv2.waitKey(1) & 0xff

    # Check if 'q' key is pressed.
    if k == ord('q'):
        # Break the loop.
        break

cap.release()
cv2.destroyAllWindows()
