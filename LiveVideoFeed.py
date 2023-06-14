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
# print("Tyring to start liveVideoFeed")
# video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# print("LiveVideoFeed has started")
# Changing the resolution
# video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# print("Done increasing video quality")
# gotten_field = False
# field = None
# Sleeping to make sure camera is focused before taking picture of the field to get better camera quality
# time.sleep(5)

# print("Video quality has been increased and the program have slept 5 seconds to focus")
# while not gotten_field:
#     ret, field_image = video.read()
#     smallGoal, bigGoal, obstacle, corners = detectField.imageRecognitionHD(video)
#     front, back, balls = detectRobotAndBalls.imageRecognitionHD(video)
#     field = Field.Field(smallGoal, bigGoal, obstacle, corners, balls, robot_modes.COLLECT)
#     gotten_field = ret
# print(field.__str__())


# As for right now this function just returns the tiniest turn just to make sure the client does not crash
# Now there is a check here if the robot needs to try and collect the balls or try to deliver the balls
def calculate_move():
    return Pathfinder.collect_balls()

# move = calculate_move()
# move.print()
