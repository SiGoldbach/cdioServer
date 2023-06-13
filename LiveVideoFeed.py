import time

import cv2

import MoveTypes
import Moves
import Pathfinder
import detectField
import Field

print("Tyring to start liveVideoFeed")
video = cv2.VideoCapture(0)
print("LiveVideoFeed has started")

video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
print("Done increasing video quality")
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


# As for right now this function just returns the tiniest turn just to make sure the client does not crash
def calculate_move():
    ret_bool, image = video.read()
    print("Video has been read")
    if ret_bool:
        try:
            return Pathfinder.collect_balls(image)
        except IndexError:
            print("Index error typically the robot can't be found or the ball array is empty ")
            return Moves.MoveClass(MoveTypes.TURN, 500, -2)


def get_image():
    get_image_ret, image = video.read()
    if not get_image_ret:
        print("Fail")

# move = calculate_move()
# move.print()
