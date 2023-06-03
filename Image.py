import cv2

import pathfinderTest


# video = cv2.VideoCapture(0, cv2.CAP_DSHOW)


def calculate_move():
    # ret, image = video.read()
    image = cv2.imread('Resources/Pictures/ballMiddle.jpg')
    return pathfinderTest.make_move(image)


calculate_move()
