import cv2 as cv
import ImFromPhoto

image = cv.imread('../Resources/Pictures/withRobot14.jpg')

balls, robot = ImFromPhoto.imageRecognition(image)
print(balls)
print(robot)
print(len(balls))
