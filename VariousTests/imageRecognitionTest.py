import cv2 as cv
import ImFromPhoto

image = cv.imread('../Resources/Pictures/Angle.jpg')

ImFromPhoto.imageRecognition(image)