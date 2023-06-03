import math
import cv2 as cv
import ImFromPhoto
import VectorTest
import moveOptions

image = cv.imread('../Resources/Pictures/ballBehind.jpg')

balls, front, back = ImFromPhoto.imageRecognition(image)
print("Result from test: ")


# print(balls)
# print(robot)
# print(len(balls))
# Trying the vectorTest


def calculate_angle2(front_pos, back_pos, target_pos):
    # Calculate the vector from the front to the back of the robot
    robot_vector = (int(back_pos[0]) - int(front_pos[0]), int(back_pos[1]) - int(front_pos[1]))

    # Calculate the vector from the front of the robot to the target position
    target_vector = (int(target_pos[0]) - int(front_pos[0]), int(target_pos[1]) - int(front_pos[1]))

    # Calculate the signed angle between the robot vector and the target vector
    angle_radians = math.atan2(target_vector[1], target_vector[0]) - math.atan2(robot_vector[1], robot_vector[0])
    angle_degrees = math.degrees(angle_radians)

    # Normalize the angle to be within the range of -180 to 180 degrees
    if angle_degrees > 180:
        angle_degrees -= 360
    elif angle_degrees < -180:
        angle_degrees += 360

    if angle_degrees < 0:
        angle_degrees = -angle_degrees
        print("right")
        print(180-angle_degrees)
        return moveOptions.RIGHT, 180 - angle_degrees

    print(180 - angle_degrees)
    return moveOptions.LEFT, 180 - angle_degrees


calculate_angle2(front, back, balls[0])
