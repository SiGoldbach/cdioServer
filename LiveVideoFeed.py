import time

import cv2

import Pathfinder
import detectField
import Field

print("Tyring to start liveVideoFeed")
video = cv2.VideoCapture(0)
print("LiveVideoFeed has started")

video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
print("Done setting vi")
gotten_field = False
field = None

time.sleep(5)

print("I got this far")
while not gotten_field:
    ret, field_image = video.read()
    smallGoal, bigGoal, obstacle = detectField.imageRecognitionHD(field_image)
    field = Field.Field(smallGoal, bigGoal, obstacle, None)
    gotten_field = ret
print(field.__str__())



def calculate_move():
    ret_bool, image = video.read()
    print("Video has been read")
    if ret_bool:
        return Pathfinder.collect_balls(image)


def get_image(counter):
    ret, image = video.read()
    if not ret:
        print("Fail")

# move = calculate_move()
# move.print()
