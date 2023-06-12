import cv2

import Pathfinder
print("Tyring to start liveVideoFeed")
video = cv2.VideoCapture(0)
print("LiveVideoFeed has started")

video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


def calculate_move():
    ret, image = video.read()
    print("Video has been read")
    if ret:
        return Pathfinder.collect_balls(image)


def get_image(counter):
    ret, image = video.read()
    if not ret:
        print("Fail")


# move = calculate_move()
# move.print()
