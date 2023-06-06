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

    red_pixels = np.sum(
        (180 <= image[..., 0]) & (image[..., 0] <= 255) & (200 <= image[..., 1]) & (50 <= image[..., 2]) &
        (image[..., 2] <= 40))
    green_mask1 = ((image[..., 0] <= 220) & (100 <= image[..., 1]) & (50 <= image[..., 2]) &
                   (image[..., 2] <= 70)).astype(np.uint8)
    # 252, 252,196
    # Blue color detection AKA front of robot
    blue_mask = ((155 <= image[..., 0]) & (255 >= image[..., 0]) & (230 <= image[..., 1]) & (255 >= image[..., 1]) & (
            170 <= image[..., 2]) & (
                         200 >= image[..., 2])).astype(np.uint8)
    blank[..., 0][blue_mask == 1] = 255
    blank[..., 1][blue_mask == 1] = 255
    blank[..., 2][blue_mask == 1] = 0

    # White color detection
    white_mask = ((220 <= image[..., 2]) & (220 <= image[..., 0]) & (220 <= image[..., 1])).astype(np.uint8)
    white_pixels = np.sum(white_mask)
    blank[..., :][white_mask == 1] = (255, 255, 255)



    # Green color detection AKA back of robot
    green_mask = ((220 >= image[..., 0]) & (100 <= image[..., 0]) & (200 <= image[..., 1]) & (170 <= image[..., 2])
                  ).astype(np.uint8)
    blank[..., 0][green_mask == 1] = 100
    blank[..., 1][green_mask == 1] = 255
    blank[..., 2][green_mask == 1] = 100

    # 18, 159, 244
    # Orange color detection
    orange_mask = (30 <= (image[..., 0]) & (140 <= image[..., 1]) & (200 >= image[..., 1]) & (
                230 <= image[..., 2])).astype(
        np.uint8)
    blank[..., 0][orange_mask == 1] = 0
    blank[..., 1][orange_mask == 1] = 150
    blank[..., 2][orange_mask == 1] = 255

    # Red color detection
    red_mask = ((170 <= image[..., 2]) & (110 >= image[..., 1])).astype(np.uint8)
    red_pixels += np.sum(red_mask)
    red_pixelLocation = []
    blank[..., 0][red_mask == 1] = 0
    blank[..., 1][red_mask == 1] = 0
    blank[..., 2][red_mask == 1] = 255

    red_pixel_indices = np.where(blank[..., 2] == 255)
    red_pixel_locations = np.column_stack(red_pixel_indices[::-1])
    print("Red pixels: " + str(len(red_pixel_locations)))

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
        minRadius=4,
        maxRadius=10
    )

    detected_Robot = cv.HoughCircles(
        gray_blurred,
        cv.HOUGH_GRADIENT,
        1,
        20,
        param1=30,
        param2=12,
        minRadius=9,
        maxRadius=20
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
            if (blank[b, a][0] == 255 & blank[b, a][1] == 255 & blank[b, a][2] == 255):
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
            if blank[b, a][0] == 100 and blank[b, a][1] == 255:
                print("CENTER OF GREEN BALL SHOULD BE: " + str(a) + " " + str(b))
                cv.circle(blank, (a, b), r, (0, 255, 100), -1)
                back.append(a)
                back.append(b)
                circle += 1
                continue
            if blank[b, a][0] == 255 and blank[b, a][1] == 255 and blank[b, a][2] == 0:
                print("CENTER OF BLUE BALL SHOULD BE: " + str(a) + " " + str(b))
                cv.circle(blank, (a, b), r, (255, 255, 0), -1)
                front.append(a)
                front.append(b)
                circle += 1
                continue

    thresh = cv.threshold(gray, 0, 150, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

    horizontal_kernel = cv.getStructuringElement(cv.MORPH_RECT, (10, 15))
    detect_horizontal = cv.morphologyEx(thresh, cv.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv.findContours(detect_horizontal, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for contour in cnts:
        x, y, w, h = cv.boundingRect(contour)
        if blank[y, x][2] == 255:
            field = cv.drawContours(blank, [contour], -1, (100, 200, 200), 2)
            M = cv.moments(contour)

            # Calculate the center of the contour
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv.line(blank, (x, cY), (cX, cY), (0, 255, 0), 2)
                cv.line(blank, (x + w, cY), (cX, cY), (255, 0, 0), 2)
                cv.circle(blank, (cX, cY), 5, (150, 150, 150), -1)
    end = time.time()

    time_for_transform = end - start

    print("Amount of red pixels: " + str(red_pixels))
    print("Amount of white pixels: " + str(white_pixels))
    print("Amount of circles: " + str(circle))

    cv.imshow('Original', image)
    cv.imshow('Obstacles and balls drawn: ', blank)

    print('Time for transform: ' + str(time_for_transform))

    cv.waitKey(0)
