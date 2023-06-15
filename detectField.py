import cv2 as cv
import numpy as np
import time


def detect_field():
    videoCapture = cv.VideoCapture(0, cv.CAP_DSHOW)
    videoCapture.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    videoCapture.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
    ret, image = videoCapture.read()
    if ret is None:
        print("No image found")

    height, width = image.shape[:2]

    blank = np.zeros((height, width, 3), dtype=np.uint8)

    start = time.time()

    img_height, img_width, _ = image.shape

    # Red color detection
    red_mask = ((170 <= image[..., 2]) & (120 >= image[..., 1]) & (160 >= image[..., 0])).astype(np.uint8)
    blank[..., 0][red_mask == 1] = 0
    blank[..., 1][red_mask == 1] = 0
    blank[..., 2][red_mask == 1] = 255

    img_gray = cv.cvtColor(blank, cv.COLOR_BGR2GRAY)
    gray = np.zeros((height, width), dtype=np.uint8)

    # Apply Gaussian blur to reduce noise
    blurred = cv.GaussianBlur(img_gray, (5, 5), 0)

    # Apply Canny edge detection
    edges = cv.Canny(blurred, 50, 150)

    # Find contours
    cnts, _ = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    smallGoal = []
    bigGoal = []
    obstacle = []
    walls = []
    done = 0

    for contour in cnts:
        x, y, w, h = cv.boundingRect(contour)

        if np.logical_and.reduce((image[y, x][2] > 100, 170 >= image[y, x][0], done == 0, w > 600)):
            epsilon = 0.01 * cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, epsilon, True)
            done = 1
            M = cv.moments(contour)

            # Calculate the center of the contour
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                # Draw field
                cv.drawContours(blank, [approx], -1, (150, 100, 255), 2)
                cv.drawContours(gray, [approx], 0, 255, thickness=cv.FILLED)
                x, y, w, h = cv.boundingRect(approx)

                # Draw path go goal from the center
                cv.line(blank, (x, cY), (cX, cY), (0, 255, 0), 2)
                cv.line(blank, (x + w, cY), (cX, cY), (255, 0, 0), 2)
                cv.circle(blank, (cX, cY), 5, (150, 150, 150), -1)
                cv.circle(blank, (x, cY), 5, (150, 150, 150), -1)

                corners = cv.goodFeaturesToTrack(gray, 4, 0.01, 400)
                for corner in corners:
                    x, y = corner.ravel().astype(int)
                    walls.append([x, y])
                    cv.circle(blank, (x, y), 5, (0, 255, 0), -1)

                # Get goals
                smallGoal.append(x)
                smallGoal.append(cY)
                bigGoal.append(x - w)
                bigGoal.append(cY)

    # detect obstacle
    for contour in cnts:
        epsilon = 0.01 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)
        x, y, w, h = cv.boundingRect(approx)
        if np.logical_and(h > 80, h < 200):
            cv.drawContours(blank, [approx], -1, (255, 100, 150), 2)

            for points in contour:
                p, t = points[0]
                obstacle.append([p, t])

    end = time.time()
    time_for_transform = end - start

    # cv.imshow('Original', image)
    # cv.imshow('State.py ', blank)

    print('Time for transform: ' + str(time_for_transform))

    # cv.waitKey(0)
    return smallGoal, bigGoal, obstacle, walls
