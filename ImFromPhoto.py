import cv2 as cv
import numpy as np
import time


def imageRecognition(image):
    if image is None:
        print("No image found")
    print(image[0][0])

    img_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    height, width = image.shape[:2]

    blank = np.zeros((height, width, 3), dtype='uint8')

    lower_red = np.array([170, 50, 180])
    upper_red = np.array([180, 255, 255])

    start = time.time()

    img_height, img_width, _ = image.shape

    red_pixels = np.sum(
        (180 <= image[..., 0]) & (image[..., 0] <= 255) & (200 <= image[..., 1]) & (50 <= image[..., 2]) &
        (image[..., 2] <= 40))
    green_mask1 = ((image[..., 0] <= 220) & (100 <= image[..., 1]) & (50 <= image[..., 2]) &
                   (image[..., 2] <= 70)).astype(np.uint8)
    blank[..., :][green_mask1 == 1] = (0, 255, 255)

    # Red color detection
    red_mask = ((200 <= image[..., 2]) & (100 >= image[..., 1])).astype(np.uint8)
    red_pixels += np.sum(red_mask)
    blank[..., 0][red_mask == 1] = 0
    blank[..., 1][red_mask == 1] = 0
    blank[..., 2][red_mask == 1] = 255

    # Orange color dectection
    orange_mask = ((120 >= image[..., 0]) & (155 <= image[..., 1]) & (190 <= image[..., 2])).astype(np.uint8)
    blank[..., 0][orange_mask == 1] = 0
    blank[..., 1][orange_mask == 1] = 150
    blank[..., 2][orange_mask == 1] = 255

    # Blue color detection AKA front of robot
    blue_mask = ((165 <= image[..., 0]) & (75 <= image[..., 1]) & (130 >= image[..., 1]) & (45 <= image[..., 2]) & (
            100 >= image[..., 2])).astype(np.uint8)
    blank[..., 0][blue_mask == 1] = 255
    blank[..., 1][blue_mask == 1] = 255
    blank[..., 2][blue_mask == 1] = 0

    # Green color detection AKA back of robot
    green_mask = ((95 <= image[..., 0]) & (150 <= image[..., 1]) & (185 >= image[..., 1]) & (80 <= image[..., 2]) & (
            120 >= image[..., 2])).astype(np.uint8)
    blank[..., 0][green_mask == 1] = 100
    blank[..., 1][green_mask == 1] = 255
    blank[..., 2][green_mask == 1] = 100

    # 108 164 100
    # White color dectection
    white_mask = ((200 <= image[..., 2]) & (200 <= image[..., 0]) & (195 <= image[..., 1])).astype(np.uint8)
    white_pixels = np.sum(white_mask)
    blank[..., :][white_mask == 1] = (255, 255, 255)

    # Circle detection
    gray = cv.cvtColor(blank, cv.COLOR_BGR2GRAY)
    gray_blurred = cv.blur(gray, (3, 3))
    detected_Balls = cv.HoughCircles(
        gray_blurred,
        cv.HOUGH_GRADIENT,
        1,
        20,
        param1=50,
        param2=13,
        minRadius=5,
        maxRadius=9
    )

    detected_Robot = cv.HoughCircles(
        gray_blurred,
        cv.HOUGH_GRADIENT,
        1,
        20,
        param1=50,
        param2=13,
        minRadius=9,
        maxRadius=12
    )
    circle = 0
    balls = []
    if detected_Balls is not None:
        detected_circles = np.uint16(np.around(detected_Balls))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            if blank[b, a][1] == 150 and blank[b, a][2] == 255:
                print("CENTER OF ORANGE BALL SHOULD BE: " + str(a) + " " + str(b))
                cv.circle(blank, (a, b), r, (0, 150, 255), -1)
                balls.append([a, b])
                circle += 1
                continue
            cv.circle(blank, (a, b), r, (255, 255, 255), -1)
            print("Center of this circle should be: " + str(a) + " " + str(b))
            balls.append([a, b])
            circle += 1
    robot = []
    if detected_Robot is not None:
        detected_circles = np.uint16(np.around(detected_Robot))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            if blank[b, a][1] == 255 and blank[b, a][2] == 100:
                print("CENTER OF GREEN BALL SHOULD BE: " + str(a) + " " + str(b))
                cv.circle(blank, (a, b), r, (130, 255, 20), -1)
                robot.append([a, b])
                circle += 1
                continue

            if blank[b, a][0] == 255 and blank[b, a][1] == 255 and blank[b, a][2] != 255:
                print("CENTER OF BLUE BALL SHOULD BE: " + str(a) + " " + str(b))
                cv.circle(blank, (a, b), r, (255, 255, 0), -1)
                robot.append([a, b])
                circle += 1
                continue

    thresh = cv.threshold(gray, 0, 150, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

    horizontal_kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 1))
    detect_horizontal = cv.morphologyEx(thresh, cv.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv.findContours(detect_horizontal, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        x, y, w, h = cv.boundingRect(c)
        if blank[y, x][2] == 255:
            cv.drawContours(blank, [c], -1, (36, 255, 12), 2)
            M = cv.moments(c)

            # Calculate the center of the contour
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

            cv.circle(blank, (cX, cY), 5, (255, 0, 0), -1)

    end = time.time()

    time_for_transform = end - start

    print("Amount of red pixels: " + str(red_pixels))
    print("Amount of white pixels: " + str(white_pixels))
    print("Amount of circles: " + str(circle))

    cv.imshow('Original', image)
    cv.imshow('Obstacles and balls drawn: ', blank)

    print('Time for transform: ' + str(time_for_transform))

    cv.waitKey(0)
    return balls, robot
