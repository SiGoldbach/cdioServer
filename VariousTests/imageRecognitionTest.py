import cv2 as cv
import ImFromPhoto

image = cv.imread('../Resources/Pictures/goal.jpg')

ImFromPhoto.imageRecognition(image)