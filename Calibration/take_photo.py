import cv2 as cv
# Simple file for capturing and saving an image in the same fashion as the image will be captured in the final display.
print("Starting")
videoCapture = cv.VideoCapture(1, cv.CAP_DSHOW)
list1 = [0]
circle_list = [0]
while 1:
    ret, image = videoCapture.read()
    if not ret:
        break
    cv.imshow('Read picture', image)
    if cv.waitKey(1) & 0xFF == ord('q'):
        cv.imwrite('Calibration/calibration_images/calibration_photo_15.jpg', image)
        break

videoCapture.release()
cv.destroyAllWindows()
