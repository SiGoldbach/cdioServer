import cv2 as cv

import detectRobotAndBalls


image = cv.imread('../Resources/Pictures/1223.jpg')

detectRobotAndBalls.imageRecognitionHD(image)
print("Result from test: ")

# print(balls)
# print(robot)
# print(len(balls))
# Trying the vectorTest


# calculate_angle2(front, back, balls[0])
