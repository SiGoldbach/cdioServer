import cv2 as cv

import detectField
import detectRobotAndBalls

image = cv.imread('../Resources/Pictures/kek.jpg')

detectRobotAndBalls.imageRecognitionHD(image)
detectField.imageRecognitionHD(image)
print("Result from test: ")

# print(balls)
# print(robot)
# print(len(balls))
# Trying the vectorTest


# calculate_angle2(front, back, balls[0])
