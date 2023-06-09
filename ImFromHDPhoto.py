import cv2 as cv
import numpy as np
import time

def imageRecognitionHD(image):
    if image is None:
        print("No image found")
        return

    height, width, _ = image.shape

    blank = np.zeros((height, width, 3), dtype='uint8')

    start = time.time()

    hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    # Fine-tune color ranges based on your specific environment
    orange_lower = np.array([0, 50, 50], dtype=np.uint8)
    orange_upper = np.array([20, 255, 255], dtype=np.uint8)

    green_lower = np.array([40, 50, 50], dtype=np.uint8)
    green_upper = np.array([90, 255, 255], dtype=np.uint8)

    blue_lower = np.array([100, 50, 50], dtype=np.uint8)
    blue_upper = np.array([130, 255, 255], dtype=np.uint8)

    red_lower1 = np.array([0, 50, 50], dtype=np.uint8)
    red_upper1 = np.array([10, 255, 255], dtype=np.uint8)

    red_lower2 = np.array([170, 50, 50], dtype=np.uint8)
    red_upper2 = np.array([180, 255, 255], dtype=np.uint8)

    # Create color masks using the updated color ranges
    orange_mask = cv.inRange(hsv_image, orange_lower, orange_upper)
    green_mask = cv.inRange(hsv_image, green_lower, green_upper)
    blue_mask = cv.inRange(hsv_image, blue_lower, blue_upper)
    red_mask1 = cv.inRange(hsv_image, red_lower1, red_upper1)
    red_mask2 = cv.inRange(hsv_image, red_lower2, red_upper2)
    red_mask = cv.bitwise_or(red_mask1, red_mask2)

    # Apply the masks to the blank image
    blank[np.where(orange_mask == 255)] = (0, 0, 255)
    blank[np.where(green_mask == 255)] = (0, 255, 100)
    blank[np.where(blue_mask == 255)] = (255, 255, 0)
    blank[np.where(red_mask == 255)] = (0, 0, 255)

    blank[np.where(red_mask == 255)] = (0, 0, 255)
    red_pixel_indices = np.column_stack(np.where(blank[..., 2] == 255))
    print("Red pixels:", len(red_pixel_indices))

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray_blurred = cv.blur(gray, (3, 3))

    detected_balls = cv.HoughCircles(
        gray_blurred,
        cv.HOUGH_GRADIENT,
        dp=1,
        minDist=20,
        param1=50,
        param2=13,
        minRadius=4,
        maxRadius=10
    )

    detected_robot = cv.HoughCircles(
        gray_blurred,
        cv.HOUGH_GRADIENT,
        dp=1,
        minDist=20,
        param1=30,
        param2=12,
        minRadius=12,
        maxRadius=17
    )

    circle = 0
    balls = []
    if detected_balls is not None:
        detected_circles = np.uint16(np.around(detected_balls))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            if 30 <= image[b, a][0] <= 140 <= image[b, a][1] <= 200 <= image[b, a][2] <= 230:
                print("CENTER OF ORANGE BALL SHOULD BE:", a, b)
                cv.circle(blank, (a, b), r, (0, 150, 255), -1)
                balls.append([a, b])
                circle += 1
                continue

            if 220 <= image[b, a][2] <= 220 <= image[b, a][0] <= 220 <= image[b, a][1]:
                cv.circle(blank, (a, b), r, (255, 255, 255), -1)
                print("Center of this circle should be:", a, b)
                balls.append([a, b])
                circle += 1

    back = []
    front = []

    if detected_robot is not None:
        detected_circles = np.uint16(np.around(detected_robot))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            if 220 >= image[b, a][0] >= 70 <= image[b, a][1] <= 200 <= image[b, a][2] <= 140:
                print("CENTER OF GREEN BALL SHOULD BE:", a, b)
                cv.circle(blank, (a, b), r, (0, 255, 100), -1)
                back.extend([a, b])
                circle += 1
                continue
            if 150 <= image[b, a][0] <= 140 <= image[b, a][1] <= 220 >= image[b, a][2] >= 120:
                print("CENTER OF BLUE BALL SHOULD BE:", a, b)
                cv.circle(blank, (a, b), r, (255, 255, 0), -1)
                front.extend([a, b])
                circle += 1
                continue

    blank_gray = cv.cvtColor(blank, cv.COLOR_BGR2GRAY)
    _, thresh = cv.threshold(blank_gray, 0, 150, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    horizontal_kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 10))
    detect_horizontal = cv.morphologyEx(thresh, cv.MORPH_OPEN, horizontal_kernel, iterations=2)
    contours, _ = cv.findContours(detect_horizontal, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        if blank[y, x][2] == 255:
            cv.drawContours(blank, [contour], -1, (100, 200, 200), 2)
            M = cv.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv.line(blank, (x, cY), (cX, cY), (0, 255, 0), 2)
                cv.line(blank, (x + w, cY), (cX, cY), (255, 0, 0), 2)
                cv.circle(blank, (cX, cY), 5, (150, 150, 150), -1)

    end = time.time()

    time_for_transform = end - start

    white_mask = ((220 <= image[..., 2]) & (220 <= image[..., 0]) & (220 <= image[..., 1])).astype(np.uint8)
    white_pixels = np.sum(white_mask)

    print("Amount of red pixels:", red_pixels)
    print("Amount of white pixels:", white_pixels)
    print("Amount of circles:", circle)

    cv.imshow('Original', image)
    cv.imshow('Obstacles and balls drawn:', blank)

    print('Time for transform:', time_for_transform)

    cv.waitKey(0)
