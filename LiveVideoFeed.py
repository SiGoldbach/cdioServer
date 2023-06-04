import cv2

import Pathfinder

video = cv2.VideoCapture(1, cv2.CAP_DSHOW)


def calculate_move():
    ret, image = video.read()
    return Pathfinder.make_move(image)

# move = calculate_move()
# move.print()
