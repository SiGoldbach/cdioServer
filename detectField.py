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
    corners = []
    done = 0
    for contour in cnts:
        x, y, w, h = cv.boundingRect(contour)
        epsilon = 0.02 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)
        if np.logical_and(image[y, x][2] > 120, np.logical_and(160 >= image[y, x][0], w > 40) & done == 0):
            if w > 500:
                cv.drawContours(blank, [approx], -1, (150, 100, 255), 2)
            M = cv.moments(contour)
            # Calculate the center of the contour
            if M["m00"] != 0 & w > 500:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                if w > 500:
                    cv.line(blank, (x, cY), (cX, cY), (0, 255, 0), 2)
                    cv.line(blank, (x + w, cY), (cX, cY), (255, 0, 0), 2)
                    cv.circle(blank, (cX, cY), 5, (150, 150, 150), -1)
                    cv.circle(blank, (x, cY), 5, (150, 150, 150), -1)

                    cv.circle(blank, (x, y), 10, (150, 150, 150), -1)
                    cv.circle(blank, (x + w, y), 10, (150, 150, 150), -1)
                    cv.circle(blank, (x, int(cY + h / 2)), 10, (150, 150, 150), -1)
                    cv.circle(blank, (x + w, int(cY + h / 2)), 10, (150, 150, 150), -1)
                    if w > 500:
                        smallGoal.append([x,cY])
                        bigGoal.append([x+w,cY])
                        corners.append([x, y])
                        corners.append([x + w, y])
                        corners.append([x, int(cY + h / 2)])
                        corners.append([x + w, int(cY + h / 2)])



    #detect obstacle
    #for contour in cnts:
        #x, y, w, h = cv.boundingRect(contour)
        #if w < 100:
            #cv.line(blank, (x, cY), (cX, cY), (0, 255, 0), 2)
            #cv.line(blank, (x + w, cY), (cX, cY), (255, 0, 0), 2)
            #cv.circle(blank, (cX, cY), 5, (150, 150, 150), -1)
            #cv.circle(blank, (x, cY), 5, (150, 150, 150), -1)

            #cv.circle(blank, (x, y), 10, (150, 150, 150), -1)
            #cv.circle(blank, (x + w, y), 10, (150, 150, 150), -1)
            #cv.circle(blank, (x, int(cY + h / 2)), 10, (150, 150, 150), -1)
            #cv.circle(blank, (x + w, int(cY + h / 2)), 10, (150, 150, 150), -1)
            #for points in contour:
            #    x, y = points[0]
            #    obstacle.append([x, y])





    end = time.time()

    time_for_transform = end - start
    print("These are the coords of the corners: ",corners)
    print("Amount of corners: " + str(len(corners)))

    cv.imshow('Original', image)
    cv.imshow('Field ', blank)

    print('Time for transform: ' + str(time_for_transform))

    cv.waitKey(0)
    return smallGoal, bigGoal, obstacle, corners
