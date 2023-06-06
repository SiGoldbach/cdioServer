import cv2 as cv

import ImFromHDPhotoNEW
import ImFromHDPhoto

image = cv.imread('../Resources/Pictures/NewHeight5.jpg')

balls, front, back, red_pixels = ImFromHDPhotoNEW.imageRecognitionHD(image)
print("Result from test: ")
print("I found: " + str(len(balls)) + " Balls")

# print(balls)
# print(robot)
# print(len(balls))
# Trying the vectorTest


# calculate_angle2(front, back, balls[0])
