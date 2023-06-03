import cv2 as cv
import ImFromPhoto

image = cv.imread('../Resources/Pictures/straight.jpg')

ImFromPhoto.imageRecognition(image)
