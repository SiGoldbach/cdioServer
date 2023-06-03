import cv2 as cv
import ImFromPhoto

image = cv.imread('../Resources/Pictures/Angle.jpg')

balls, robot = ImFromPhoto.imageRecognition(image)
print(balls)
print(robot)
print(len(balls))
