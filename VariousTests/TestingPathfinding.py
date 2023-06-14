# This file is for testing the Pathfinder algorithm we have implemented.
# This is not much of a black box test
# This

import cv2
import Pathfinder

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
print("LiveVideoFeed has started")
# Changing the resolution
video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
move = Pathfinder.deliver_balls(video)
move.print()
