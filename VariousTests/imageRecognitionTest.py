import cv2 as cv

import detectRobotAndBalls
import detectField

image = cv.imread('../Resources/Pictures/kek6.jpg')

detectField.imageRecognitionHD(image)
print("Result from test: ")

# print(balls)
# print(robot)
# print(len(balls))
# Trying the vectorTest


# calculate_angle2(front, back, balls[0])
