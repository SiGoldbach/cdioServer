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


    # Red color detection
    red_mask = ((170 <= image[..., 2]) & (120 >= image[..., 1]) & (160 >= image[..., 0])).astype(np.uint8)
    blank[..., 0][red_mask == 1] = 0
    blank[..., 1][red_mask == 1] = 0
    blank[..., 2][red_mask == 1] = 255

    img_gray = cv.cvtColor(blank, cv.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv.GaussianBlur(img_gray, (5, 5), 0)

    # Apply Canny edge detection
    edges = cv.Canny(blurred, 50, 150)
    # Find contours
    cnts, _ = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    smallGoal = []
    bigGoal = []
    obstacle = []
    corn = []
    for contour in cnts:
        x, y, w, h = cv.boundingRect(contour)
        epsilon = 0.01 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)
        print(image[y, x][2], image[y, x][0])
        if np.logical_and(image[y, x][2] > 100, np.logical_and(170 >= image[y, x][0], w > 40)):
            M = cv.moments(contour)

            # Calculate the center of the contour
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                if M["m00"] != 0:
                    cv.drawContours(blank, [approx], -1, (150, 100, 255), 2)
                    cv.line(blank, (x, cY), (cX, cY), (0, 255, 0), 2)
                    cv.line(blank, (x + w, cY), (cX, cY), (255, 0, 0), 2)
                    cv.circle(blank, (cX, cY), 5, (150, 150, 150), -1)
                    cv.circle(blank, (x, cY), 5, (150, 150, 150), -1)

                    #cv.circle(blank, (x, y), 10, (150, 150, 150), -1)
                    #cv.circle(blank, (x + w, y), 10, (150, 150, 150), -1)
                    #cv.circle(blank, (x, int(cY + h / 2)), 10, (150, 150, 150), -1)
                    #cv.circle(blank, (x + w, int(cY + h / 2)), 10, (150, 150, 150), -1)
                    corners = cv.goodFeaturesToTrack(blurred, 4, 0.001, 600)
                    corners = np.int0(corners)

                    smallGoal.append([x, cY])
                    bigGoal.append([x + w, cY])









    #detect obstacle
    for contour in cnts:
        x, y, w, h = cv.boundingRect(contour)
        if w < 100 & w > 20:
            cv.line(blank, (x, cY), (cX, cY), (0, 255, 0), 2)
            cv.line(blank, (x + w, cY), (cX, cY), (255, 0, 0), 2)
            cv.circle(blank, (cX, cY), 5, (150, 150, 150), -1)
            cv.circle(blank, (x, cY), 5, (150, 150, 150), -1)

            cv.circle(blank, (x, y), 10, (150, 150, 150), -1)
            cv.circle(blank, (x + w, y), 10, (150, 150, 150), -1)
            cv.circle(blank, (x, int(cY + h / 2)), 10, (150, 150, 150), -1)
            cv.circle(blank, (x + w, int(cY + h / 2)), 10, (150, 150, 150), -1)
            for points in contour:
                x, y = points[0]
                obstacle.append([x, y])





    end = time.time()

    time_for_transform = end - start
    print("These are the coords of the corners: ",corn)

    cv.imshow('Original', image)
    cv.imshow('Field ', blank)

    print('Time for transform: ' + str(time_for_transform))

    cv.waitKey(0)
    return smallGoal, bigGoal, obstacle, corn
