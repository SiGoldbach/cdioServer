import Pathfinder
import cv2 as cv

image = cv.imread('../Resources/Pictures/kek.jpg')
Pathfinder.drive_to_goal(image)