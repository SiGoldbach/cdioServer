import cv2 as cv
import pathfinderTest

image = cv.imread('../Resources/Pictures/withRobot14.jpg')
if image is None:
    print("None")
pathfinderTest.make_move(image)

# I am here checking the angle function
#pathfinderTest.turnAngleWithVectors([[2, 3], [-3, 2]], [-3, 2])
