import cv2

import Pathfinder

video = cv2.VideoCapture(1, cv2.CAP_DSHOW)

video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


def calculate_move():
    ret, image = video.read()
    print("Video has been read")
    if ret:
        return Pathfinder.make_move(image)


def get_image(counter):
    print("I am in function")
    ret, image = video.read()
    if ret:
        print("Success")
        cv2.imwrite('Resources/Pictures/WRITEFFS' + str(counter) + '.jpg', image)
        counter += 1

    return image

# move = calculate_move()
# move.print()
