import cv2 as cv
import numpy as np
import time


def imageRecognitionHD(image):
    if image is None:
        print("No image found")

    height, width = image.shape[:2]

    blank = np.zeros((height, width, 3), dtype=np.uint8)

    start = time.time()


    img_height, img_width, _ = image.shape

    # Circle detection
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray_blurred = cv.blur(gray, (3, 3))
    detected_Balls = cv.HoughCircles(
        gray_blurred,
        cv.HOUGH_GRADIENT,
        1,
        20,
        param1=50,
        param2=13,
        minRadius=9,
        maxRadius=11
    )

    detected_Robot = cv.HoughCircles(
        gray_blurred,
        cv.HOUGH_GRADIENT,
        1,
        20,
        param1=30,
        param2=12,
        minRadius=15,
        maxRadius=17
    )
    circle = 0
    balls = []

    # White color detection
    white_mask = ((220 <= image[..., 2]) & (220 <= image[..., 0]) & (220 <= image[..., 1])).astype(np.uint8)
    white_pixels = np.sum(white_mask)

    if detected_Balls is not None:
        detected_circles = np.uint16(np.around(detected_Balls))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            if np.logical_and.reduce(
                    (50 >= image[b, a][0], 160 <= image[b, a][1], 200 >= image[b, a][1], 160 <= image[b, a][2])):
                print("CENTER OF ORANGE BALL SHOULD BE: " + str(a) + " " + str(b))
                cv.circle(blank, (a, b), r, (0, 150, 255), -1)
                balls.append([a, b])
                circle += 1
                continue

            if np.logical_and.reduce((200 <= image[b, a][2], 200 <= image[b, a][0], 200 <= image[b, a][1])):
                cv.circle(blank, (a, b), r, (255, 255, 255), -1)
                print("Center of this circle should be: " + str(a) + " " + str(b))
                balls.append([a, b])
                circle += 1

    back = []
    front = []

    if detected_Robot is not None:
        detected_circles = np.uint16(np.around(detected_Robot))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            if np.logical_and.reduce(
                    (220 >= image[b, a][0], 70 <= image[b, a][0], 200 <= image[b, a][1], 140 <= image[b, a][2])):
                print("CENTER OF GREEN BALL SHOULD BE: " + str(a) + " " + str(b))
                cv.circle(blank, (a, b), r, (0, 255, 100), -1)
                back.append(a)
                back.append(b)
                circle += 1
                continue
            if np.logical_and.reduce((150 <= image[b, a][0], 140 <= image[b, a][1], 255 >= image[b, a][1],
                                      120 <= image[b, a][2], 220 >= image[b, a][2])):
                print("CENTER OF BLUE BALL SHOULD BE: " + str(a) + " " + str(b))
                cv.circle(blank, (a, b), r, (255, 255, 0), -1)
                front.append(a)
                front.append(b)
                circle += 1
                continue


    end = time.time()

    time_for_transform = end - start
    print("Amount of white pixels: " + str(white_pixels))
    print("Amount of circles: " + str(circle))
    print("Amount of balls: " + str(len(balls)))
    cv.imshow('Original', image)
    cv.imshow('Obstacles and balls drawn: ', blank)

    print('Time for transform: ' + str(time_for_transform))

    cv.waitKey(0)
    return front, back, balls
