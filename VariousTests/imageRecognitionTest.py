import cv2 as cv

import detectRobotAndBalls
import ImFromHDPhoto
import detectField

image = cv.imread('../Resources/Pictures/NewHeight10.jpg')

detectRobotAndBalls.imageRecognitionHD(image)
print("Result from test: ")

# print(balls)
# print(robot)
# print(len(balls))
# Trying the vectorTest


# calculate_angle2(front, back, balls[0])
