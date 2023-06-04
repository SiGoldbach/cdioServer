import math
import cv2 as cv
import ImFromPhoto
import MoveTypes

image = cv.imread('../Resources/Pictures/testRun1.jpg')

balls, front, back = ImFromPhoto.imageRecognition(image)
print("Result from test: ")


# print(balls)
# print(robot)
# print(len(balls))
# Trying the vectorTest



# calculate_angle2(front, back, balls[0])
