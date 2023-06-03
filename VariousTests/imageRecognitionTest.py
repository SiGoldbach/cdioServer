import cv2 as cv
import ImFromPhoto

image = cv.imread('../Resources/Pictures/Obs.jpg')

balls, robot = ImFromPhoto.imageRecognition(image)
print("Result from test: ")
print(balls)
print(robot)
print(len(balls))
