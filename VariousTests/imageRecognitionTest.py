import cv2 as cv

import ImFromPhoto

image = cv.imread('../Resources/Pictures/CheckForObstacle3.jpg')

balls, front, back = ImFromPhoto.imageRecognition(image)
print("Result from test: ")
print("I found: "+str(len(balls))+" Balls")


# print(balls)
# print(robot)
# print(len(balls))
# Trying the vectorTest


# calculate_angle2(front, back, balls[0])
