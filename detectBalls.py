import cv2 as cv
import numpy as np
import time
import Calibration.cameraCalibrationv2 as calibration


# Image recognition now takes a videoInput instead of a frame, so it does not return anything and wait until
# the robot is found
def detect_balls():
    videoCapture = cv.VideoCapture(0, cv.CAP_DSHOW)  # 0 is the default camera
    videoCapture.set(cv.CAP_PROP_FRAME_WIDTH, 1280)  # 1280x720 is the default resolution
    videoCapture.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
    while 1:  # Loop until the robot is found
        balls = []
        ret, image = videoCapture.read()  # Read the image from the camera
        image = calibration.continuous_undistortion(image)  # Undistort the image using the calibration data

        if ret is None:
            print("No image was found")

        height, width = image.shape[:2]  # Get the height and width of the image

        blank = np.zeros((height, width, 3), dtype=np.uint8)  # Create a blank image to draw on

        img_height, img_width, _ = image.shape  # Get the height and width of the image

        start = time.time()

        # Circle detection
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)  # Convert the image to HSV

        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)  # Convert the image to grayscale
        gray_blurred = cv.blur(gray, (3, 3))  # Blur the image to reduce noise

        detected_Balls = cv.HoughCircles(
            gray_blurred,
            cv.HOUGH_GRADIENT,
            1,
            20,
            param1=70,
            param2=12,
            minRadius=8,
            maxRadius=11
        )

        circle = 0

        if detected_Balls is not None:
            detected_circles = np.uint16(np.around(detected_Balls))  # Get the detected circles

            for pt in detected_circles[0, :]:  # For each circle
                a, b, r = pt[0], pt[1], pt[2]  # Get the center and radius of the circle
                if a < img_width and b < img_height:  # If the circle is within the image
                    hsv_pixel = hsv[b, a]  # Get the HSV value of the pixel

                # Orange color range in HSV
                orange_lower = np.array([0, 50, 50], dtype=np.uint8)
                orange_upper = np.array([20, 255, 255], dtype=np.uint8)

                if np.all(cv.inRange(hsv_pixel, orange_lower, orange_upper)):  # If the pixel is orange
                    print("CENTER OF ORANGE BALL SHOULD BE: " + str(a) + " " + str(b))
                    cv.circle(blank, (a, b), r, (0, 150, 255), -1)  # Draw a circle on the blank image
                    balls.append([a, b]) # Add the center of the circle to the list of balls
                    circle += 1
                    continue

                # White color range in HSV
                white_lower = np.array([0, 0, 200], dtype=np.uint8)
                white_upper = np.array([179, 30, 255], dtype=np.uint8)

                if np.all(cv.inRange(hsv_pixel, white_lower, white_upper)):  # If the pixel is white
                    cv.circle(blank, (a, b), r, (255, 255, 255), -1)  # Draw a circle on the blank image
                    print("CENTER OF WHITE BALL SHOULD BE: " + str(a) + " " + str(b))
                    balls.append([a, b])  # Add the center of the circle to the list of balls
                    circle += 1

        end = time.time()

        time_for_transform = end - start
        print("Amount of circles: " + str(circle))
        print("Amount of balls: " + str(len(balls)))
        print('Time for transform: ' + str(time_for_transform))

        # cv.waitKey(0)
        if len(balls) > 0:  # If the robot is found
            return balls
