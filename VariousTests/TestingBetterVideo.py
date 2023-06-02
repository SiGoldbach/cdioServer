import cv2

cap = cv2.VideoCapture(1)

while True:
    # Capture image frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        height, width = frame.shape[:2]
        print("Height: " + height + " Width: " + width)
        break

    # When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
