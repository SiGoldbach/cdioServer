import cv2 as cv

import ImFromHDPhotoNEW
import ImFromHDPhoto
import detectField

image = cv.imread('../Resources/Pictures/caliResult1.jpg')

front, back,balls, red_pixels = detectField.imageRecognitionHD(image)
print("Result from test: ")
print("I found: " + str(len(balls)) + " Balls")

# print(balls)
# print(robot)
# print(len(balls))
# Trying the vectorTest


# calculate_angle2(front, back, balls[0])
