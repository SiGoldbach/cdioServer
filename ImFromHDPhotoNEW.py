import cv2 as cv
import numpy as np
import time


def imageRecognitionHD(image):
    if image is None:
        print("No image found")

    height, width = image.shape[:2]

    blank = np.zeros((height, width, 3), dtype='uint8')

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
        maxRadius=10
    )

    detected_Robot = cv.HoughCircles(
        gray_blurred,
        cv.HOUGH_GRADIENT,
        1,
        20,
        param1=30,
        param2=12,
        minRadius=12,
        maxRadius=17
    )
    circle = 0
    balls = []

    # White color detection
    white_mask = ((220 <= image[..., 2]) & (220 <= image[..., 0]) & (220 <= image[..., 1])).astype(np.uint8)
    white_pixels = np.sum(white_mask)

    red_pixels = np.sum(
        (180 <= image[..., 0]) & (image[..., 0] <= 255) & (200 <= image[..., 1]) & (50 <= image[..., 2]) &
        (image[..., 2] <= 40))
    # Red color detection
    red_mask = ((170 <= image[..., 2]) & (120 >= image[..., 1]) & (160 >= image[..., 0])).astype(np.uint8)
    red_pixels += np.sum(red_mask)
    blank[..., 0][red_mask == 1] = 0
    blank[..., 1][red_mask == 1] = 0
    blank[..., 2][red_mask == 1] = 255

    if detected_Balls is not None:
        detected_circles = np.uint16(np.around(detected_Balls))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            if 30 <= (image[b, a][0]) & (140 <= image[b, a][1]) & (200 >= image[b, a][1]) & (
                    230 <= image[b, a][2]):
                print("CENTER OF ORANGE BALL SHOULD BE: " + str(a) + " " + str(b))
                cv.circle(blank, (a, b), r, (0, 150, 255), -1)
                balls.append([a, b])
                circle += 1
                continue

            if (220 <= image[b, a][2]) & (220 <= image[b, a][0]) & (220 <= image[b, a][1]):
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
            if (220 >= image[b, a][0]) & (70 <= image[b, a][0]) & (200 <= image[b, a][1]) & (140 <= image[b, a][2]):
                print("CENTER OF GREEN BALL SHOULD BE: " + str(a) + " " + str(b))
                cv.circle(blank, (a, b), r, (0, 255, 100), -1)
                back.append(a)
                back.append(b)
                circle += 1
                continue
            if (150 <= image[b, a][0]) & (140 <= image[b, a][1]) & (230 >= image[b, a][1]) & (120 <= image[b, a][2]):
                print("CENTER OF BLUE BALL SHOULD BE: " + str(a) + " " + str(b))
                cv.circle(blank, (a, b), r, (255, 255, 0), -1)
                front.append(a)
                front.append(b)
                circle += 1
                continue

    img_gray = cv.cvtColor(blank, cv.COLOR_BGR2GRAY)

    # Thresholding
    _, thresh = cv.threshold(img_gray, 10, 250, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # Find contours
    cnts, _ = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    smallGoal = []
    for contour in cnts:
        x, y, w, h = cv.boundingRect(contour)
        print("HEllo")
        if image[y, x][2] < 235:
            cv.drawContours(blank, [contour], -1, (150, 100, 255), 2)
            M = cv.moments(contour)

            # Calculate the center of the contour
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                if(w > 500):
                    cv.line(blank, (x, cY), (cX, cY), (0, 255, 0), 2)
                    cv.line(blank, (x + w, cY), (cX, cY), (255, 0, 0), 2)
                    cv.circle(blank, (cX, cY), 5, (150, 150, 150), -1)
                    cv.circle(blank, (x, cY), 5, (150, 150, 150), -1)
                    smallGoal.append(x)
                    smallGoal.append(cY)
                    break



    end = time.time()

    time_for_transform = end - start

    print("Amount of red pixels: " + str(red_pixels))
    print("Amount of white pixels: " + str(white_pixels))
    print("Amount of circles: " + str(circle))

    cv.imshow('Original', image)
    cv.imshow('Obstacles and balls drawn: ', blank)

    print('Time for transform: ' + str(time_for_transform))

    cv.waitKey(0)
    return front, back, balls, smallGoal

