import cv2 as cv
import numpy as np
import time
import Calibration.cameraCalibrationv2

# Image recognition now takes a videoInput instead of a frame, so it does not return anything and wait until the
# robot is found
def detect_robot():
    videoCapture = cv.VideoCapture(1, cv.CAP_DSHOW)
    videoCapture.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    videoCapture.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
    while 1:
        back = []
        front = []
        ret, image = videoCapture.read()
        image = Calibration.cameraCalibrationv2.continuous_undistortion(image)

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

        detected_Front = cv.HoughCircles(
            gray_blurred,
            cv.HOUGH_GRADIENT,
            1,
            20,
            param1=30,
            param2=20,
            minRadius=21,
            maxRadius=24
        )

        detected_Back = cv.HoughCircles(
            gray_blurred,
            cv.HOUGH_GRADIENT,
            1,
            20,
            param1=30,
            param2=20,
            minRadius=14,
            maxRadius=18
        )

        circle = 0

        if detected_Front is not None:
            detected_circles = np.uint16(np.around(detected_Front))
            for pt in detected_circles[0, :]:
                a, b, r = pt[0], pt[1], pt[2]
                if a < img_width and b < img_height:
                    hsv_pixel = hsv[b, a]

                # Blue color range in HSV
                blue_lower = np.array([100, 100, 100], dtype=np.uint8)
                blue_upper = np.array([120, 255, 255], dtype=np.uint8)

                if np.all(cv.inRange(hsv_pixel, blue_lower, blue_upper)):
                    print("CENTER OF BLUE BALL SHOULD BE: " + str(a) + " " + str(b))
                    cv.circle(blank, (a, b), r, (255, 255, 0), -1)
                    front.append(a)
                    front.append(b)
                    circle += 1
                    continue

        if detected_Back is not None:
            detected_circles = np.uint16(np.around(detected_Back))
            for pt in detected_circles[0, :]:
                a, b, r = pt[0], pt[1], pt[2]
                if a < img_width and b < img_height:
                    hsv_pixel = hsv[b, a]

                # Green color range in HSV
                green_lower = np.array([30, 50, 50], dtype=np.uint8)
                green_upper = np.array([120, 255, 255], dtype=np.uint8)

                if np.all(cv.inRange(hsv_pixel, green_lower, green_upper)):
                    print("CENTER OF GREEN BALL SHOULD BE: " + str(a) + " " + str(b))
                    cv.circle(blank, (a, b), r, (0, 255, 100), -1)
                    back.append(a)
                    back.append(b)
                    circle += 1
                    continue

        end = time.time()

        time_for_transform = end - start
        print("Amount of circles: " + str(circle))
        # cv.imshow('Original', image)
        # cv.imshow('Obstacles and balls drawn: ', blank)
        print(len(front))
        print(len(back))
        print('Time for transform: ' + str(time_for_transform))

        # cv.waitKey(0)
        if len(front) == 2 and len(back) == 2:
            return front, back
