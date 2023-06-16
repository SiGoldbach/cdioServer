import cv2 as cv
import numpy as np
import time
import Calibration.cameraCalibrationv2 as calibration


# Image recognition now takes a videoInput instead of a frame, so it does not return anything and wait until
# the robot is found
def detect_balls():
    videoCapture = cv.VideoCapture(0, cv.CAP_DSHOW)
    videoCapture.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    videoCapture.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
    while 1:
        balls = []
        back = []
        front = []
        ret, image = videoCapture.read()
        image = calibration.continuous_undistortion(image)

        if ret is None:
            print("No image found")

        height, width = image.shape[:2]

        blank = np.zeros((height, width, 3), dtype=np.uint8)

        start = time.time()

        img_height, img_width, _ = image.shape

        # Circle detection
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        gray_blurred = cv.blur(gray, (3, 3))

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
            detected_circles = np.uint16(np.around(detected_Balls))

            for pt in detected_circles[0, :]:
                a, b, r = pt[0], pt[1], pt[2]
                if a < img_width and b < img_height:
                    hsv_pixel = hsv[b, a]

                # Orange color range in HSV
                orange_lower = np.array([10, 70, 50], dtype=np.uint8)
                orange_upper = np.array([35, 255, 255], dtype=np.uint8)

                if np.all(cv.inRange(hsv_pixel, orange_lower, orange_upper)):
                    print("CENTER OF ORANGE BALL SHOULD BE: " + str(a) + " " + str(b))
                    cv.circle(blank, (a, b), r, (0, 150, 255), -1)
                    balls.append([a, b])
                    circle += 1
                    continue

                # White color range in HSV
                white_lower = np.array([0, 0, 200], dtype=np.uint8)
                white_upper = np.array([179, 30, 255], dtype=np.uint8)

                if np.all(cv.inRange(hsv_pixel, white_lower, white_upper)):
                    cv.circle(blank, (a, b), r, (255, 255, 255), -1)
                    print("Center of this circle should be: " + str(a) + " " + str(b))
                    balls.append([a, b])
                    circle += 1

        end = time.time()

        time_for_transform = end - start
        print("Amount of circles: " + str(circle))
        print("Amount of balls: " + str(len(balls)))
        print('Time for transform: ' + str(time_for_transform))

        # cv.waitKey(0)
        if len(balls) > 0:
            return balls
