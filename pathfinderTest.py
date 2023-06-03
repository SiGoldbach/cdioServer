import math

import numpy as np

import MoverFinder
import moveOptions
import ImFromPhoto

# import main


goal_x = 0
goal_y = 0


def find_nearest_ball(robot_location, ball_locations):
    closest_distance = float('inf')
    closest_coordinate = []
    r1 = int(robot_location[1][0])
    r2 = int(robot_location[1][1])

    for coordinate in ball_locations:
        x = int(coordinate[0])
        y = int(coordinate[1])
        print((x - r1) ** 2 + (y - r2) ** 2)
        distance = math.sqrt((x - r1) ** 2 + (y - r2) ** 2)

        if distance < closest_distance:
            closest_distance = distance
            closest_coordinate = coordinate

    return closest_coordinate, closest_distance


def calculate_angle(ball_x, ball_y, robot_x, robot_y):
    angle = math.atan2(ball_y - robot_y, ball_x - robot_x) * (180 / math.pi)
    return angle


def calculate_angle2(robot_location, ball_location):
    r1 = int(robot_location[1][0])
    r2 = int(robot_location[1][1])
    r21 = int(robot_location[0][0])
    r22 = int(robot_location[0][1])
    A = math.sqrt((ball_location[0] - r1) ** 2 + (ball_location[1] - r2) ** 2)
    B = math.sqrt((r21 - r1) ** 2 + (r22 - r2) ** 2)
    C = math.sqrt((ball_location[0] - r21) ** 2 + (ball_location[1] - r22) ** 2)
    return math.degrees(math.acos((A * A + B * B - C * C) / (2.0 * A * B)))


# This function finds the angle between the two vector that are ass to ball and ass to head
def turnAngleWithVectors(robot_location, ball_location):
    ass = robot_location[0]
    head = robot_location[1]
    head_vector = [int(head[0]) - int(ass[0]), int(head[1]) - int(ass[1])]
    ball_vector = [int(ball_location[0] - int(ass[0])), int(ball_location[1]) - int(ass[1])]
    neutralVector = [1, 0]

    print("Vector describing the robot: " + str(head_vector))
    print("Vector describing the ass to ball relation: " + str(ball_vector))

    unit_vector_1 = head_vector / np.linalg.norm(head_vector)
    unit_vector_2 = ball_vector / np.linalg.norm(ball_vector)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    print("Dot product of vectors: " + str(dot_product))
    angle = np.arccos(dot_product)

    print("Angle should be: " + str(angle))
    return angle

def is_point_left_or_right(robot_location, ball_location):
    r1 = int(robot_location[1][0])
    r2 = int(robot_location[1][1])
    r21 = int(robot_location[0][0])
    r22 = int(robot_location[0][1])



def find_goal_distance(goal_x, goal_y, robot_x, robot_y):
    goal_distance = math.sqrt((goal_x - robot_x) ** 2 + (goal_y - robot_y) ** 2)
    return goal_distance


# Robotens røv er første punkt
def make_move(image):
    ball_locations = [[2, 4], [2, 3], [8, 8], [8, 3], [10, 10], [20, 20], [1, 9], [16, 14]]  # Example of table balls
    orange_ball = [0, 0]  # the orange ball
    robot_location = [0, 0]  # example of robot location
    print("Now doing image recognition")
    ball_locations, robot_location = ImFromPhoto.imageRecognition(image)

    obstacles = [[5, 5], [5, 6], [5, 7], [5, 8], [5, 9]]  # Example obstacle coordinates (representing a wall)
    grid_size = [21, 21]  # Grid size representing the workspace
    closest_ball_location, distanceToBall = find_nearest_ball(robot_location, ball_locations)
    print("Closest ball: " + str(closest_ball_location))
    print("Robot location" + str(robot_location))
    angle_to_turn = calculate_angle2(robot_location, closest_ball_location)
    closest_ball_location[0] = closest_ball_location[0] - 20
    closest_ball_location[1] = closest_ball_location[1] - 20
    angle_to_turn2 = turnAngleWithVectors(robot_location, closest_ball_location)

    print("The angle between me and the ball is: " + str(angle_to_turn))
    print("The angle between me and the ball is: " + str(angle_to_turn2))

    angle_to_goal = calculate_angle(goal_x, goal_y, robot_location[0], robot_location[1])
    goalDistance = find_goal_distance(goal_x, goal_y, robot_location[0], robot_location[1])

    if angle_to_goal > 0 & len(ball_locations) == 5 | 3 | 2 | 1:
        return MoverFinder.MoveClass(moveOptions.RIGHT, 300, angle_to_goal), MoverFinder.MoveClass(moveOptions.FORWARD,
                                                                                                   500, goalDistance)
    if angle_to_goal < 0 & len(ball_locations) == 5 | 3 | 2 | 1:
        return MoverFinder.MoveClass(moveOptions.LEFT, 300, angle_to_goal), MoverFinder.MoveClass(moveOptions.FORWARD,
                                                                                                  500, goalDistance)
    if angle_to_goal == 0 & len(ball_locations) == 5 | 3 | 2 | 1:
        return MoverFinder.MoveClass(moveOptions.FORWARD, 500, goalDistance)

    if angle_to_turn > 0:
        return MoverFinder.MoveClass(moveOptions.RIGHT, 300, angle_to_turn), MoverFinder.MoveClass(moveOptions.FORWARD,
                                                                                                   500, distanceToBall)
    if angle_to_turn == 0:
        return MoverFinder.MoveClass(moveOptions.FORWARD, 500, distanceToBall)

    if angle_to_turn < 0:
        return MoverFinder.MoveClass(moveOptions.LEFT, 300, angle_to_turn), MoverFinder.MoveClass(moveOptions.FORWARD,
                                                                                                  500, distanceToBall)

    return MoverFinder.MoveClass(moveOptions.UNSTUCK, 500, 100)
