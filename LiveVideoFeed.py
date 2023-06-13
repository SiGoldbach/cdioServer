import time

import cv2

import MoveTypes
import Moves
import Pathfinder
import detectField
import Field
import detectRobotAndBalls
import robot_modes

# Setting up the video feed
print("Tyring to start liveVideoFeed")
video = cv2.VideoCapture(0)
print("LiveVideoFeed has started")
# Changing the resolution
video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
print("Done increasing video quality")
gotten_field = False
field = None
# Sleeping to make sure camera is focused before taking picture of the field to get better camera quality
time.sleep(5)

print("Video quality has been increased and the program have slept 5 seconds to focus")
while not gotten_field:
    ret, field_image = video.read()
    smallGoal, bigGoal, obstacle, corners = detectField.imageRecognitionHD(field_image)
    front, back, balls = detectRobotAndBalls.imageRecognitionHD(field_image)
    field = Field.Field(smallGoal, bigGoal, obstacle, corners, balls, robot_modes.DELIVER)
    gotten_field = ret
print(field.__str__())


# As for right now this function just returns the tiniest turn just to make sure the client does not crash
# Now there is a check here if the robot needs to try and collect the balls or try to deliver the balls
def calculate_move():
    ret_bool, image = video.read()
    if ret_bool:
        print("Image has been read")
        try:
            if field.mode == robot_modes.COLLECT:
                return Pathfinder.collect_balls(image)
            if field.mode != robot_modes.COLLECT:
                return Pathfinder.deliver_balls(image, field)
        except IndexError:
            print("Index error typically the robot can't be found or the ball array is empty ")
            return Moves.MoveClass(MoveTypes.TURN, 500, -5)
    else:
        return Moves.MoveClass(MoveTypes.TURN, 500, 5)


def get_image():
    get_image_ret, image = video.read()
    if not get_image_ret:
        print("Fail")

# move = calculate_move()
# move.print()
