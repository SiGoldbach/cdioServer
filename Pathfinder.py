import math

import ImFromPhoto
import Moves
import MoveTypes


# import main


def find_nearest_ball(front, ball_locations):
    closest_distance = float('inf')
    closest_coordinate = []
    r1 = int(front[0])
    r2 = int(front[1])

    for coordinate in ball_locations:
        x = int(coordinate[0])
        y = int(coordinate[1])
        print((x - r1) ** 2 + (y - r2) ** 2)
        distance = math.sqrt((x - r1) ** 2 + (y - r2) ** 2)

        if distance < closest_distance:
            closest_distance = distance
            closest_coordinate = coordinate

    return closest_coordinate, closest_distance


# This function finds the angle between the two vector that are ass to ball and ass to head


def calculate_turn(front_pos, back_pos, target_pos):
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
        # print("right")
        # print(180 - angle_degrees)
        return MoveTypes.RIGHT, 180 - angle_degrees

    # print(180 - angle_degrees)
    return MoveTypes.LEFT, 180 - angle_degrees


def degree_to_argument(degrees):
    print("Calculating argument ")
    argumentTurn = (degrees - -5.862845) / 0.209388
    return int(argumentTurn) / 2


def find_goal_distance(goal_x, goal_y, robot_x, robot_y):
    goal_distance = math.sqrt((goal_x - robot_x) ** 2 + (goal_y - robot_y) ** 2)
    return goal_distance


# This function is being written iteratively.
# Meaning only moves which we have a realistic chance of taking are added to the control flow
# At current time:
# The robot can turn and align itself to a ball
# It can move forward if is aligned
def make_move(image):
    print("Now doing image recognition")
    ball_locations, front, back = ImFromPhoto.imageRecognition(image)
    # Temporary if statement
    if front is None or back is None or ball_locations is None:
        return Moves.MoveClass(MoveTypes.LEFT, 500, 50)
    nearest_ball, distance = find_nearest_ball(front, ball_locations)

    angle_to_turn = calculate_turn(front, back, nearest_ball)

    if angle_to_turn[1] > 6:
        print("I should turn: " + angle_to_turn[0])
        print(str(angle_to_turn[1]) + " degrees")
        argument = degree_to_argument(angle_to_turn[1])
        return Moves.MoveClass(angle_to_turn[0], 500, argument)

    else:
        print("I am aligned and should move forward")
        return Moves.MoveClass(MoveTypes.FORWARD, 600, 1500)
