import cv2 as cv
import ImFromPhoto

image = cv.imread('../Resources/Pictures/withRobot14.jpg')

ImFromPhoto.imageRecognition(image)