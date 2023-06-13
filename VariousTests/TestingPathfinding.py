# This file is for testing the Pathfinder algorithm we have implemented.
# This is not much of a black box test
# This

import cv2 as cv
import Pathfinder

image = cv.imread('../Resources/Pictures/dist2.jpg')
if image is None:
    print("None")
move = Pathfinder.collect_balls(image)
move.print()
