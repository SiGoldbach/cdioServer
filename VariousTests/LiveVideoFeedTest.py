import time
import numpy as np
import cv2

import detectRobot

video = cv2.VideoCapture(1, cv2.CAP_DSHOW)

video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
ret, frame = video.read()

detectRobotAndBalls.imageRecognitionHD(frame)


