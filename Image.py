import cv2
import Pathfinding

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)


def calculate_move():
    ret, image = video.read()
    if ret:
        print("image has been read")
        cv2.imwrite('Resources/CapturedPic.jpg', image)
        Pathfinding.next_move(image)


calculate_move()
