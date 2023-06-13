import math
import Pathfinder
import numpy as np

np.set_printoptions(precision=3, suppress=True)


def calculate_obstacle_angle(back_pos, front_pos, obstacles, side):
    robot_middle = robot_mid_edge(front_pos, back_pos, side)
    robot_front = robot_front_edge(front_pos, back_pos, side)
    angles = []

    for obstacle in Pathfinder.find_obstacle_in_circle(obstacles, front_pos, back_pos):
        angle = getAngle(robot_front, robot_middle, obstacle)
        if side == "left":
            if angle > 0:
                angles.append(angle)  # Add the angle to the array

        if side == "right":
            if angle < 0:
                angles.append(angle)

    smallest_angle = min(angles)  # Find the smallest angle in the array
    largest_angle = max(angles)
    return smallest_angle, largest_angle


def getAngle(F, D, O):
    ang = math.degrees(math.atan2(O[1] - D[1], O[0] - D[0]) - math.atan2(F[1] - D[1], F[0] - D[0]))
    return ang


def robot_front_edge(front_pos, back_pos, side):
    # Calculate the vector representing the direction of the robot
    robot_direction = (front_pos[0] - back_pos[0], front_pos[1] - back_pos[1])

    angle_radians = math.atan2(robot_direction[1], robot_direction[0]) * -1

    point_difference = (
        (Pathfinder.robot_width() / 2) * math.sin(angle_radians),
        Pathfinder.robot_width() / 2 * math.cos(angle_radians))
    robot_center = front_pos

    # HAVE TO MAKE SURE THAT "left" AND "right" ARE CORRECT WITH WHAT WAY TO TURN
    if side == "left":
        new_point = round(robot_center[0] + point_difference[0], 3), round(robot_center[1] + point_difference[1], 3)
        return new_point
    if side == "right":
        new_point = round(robot_center[0] - point_difference[0], 3), round(robot_center[1] - point_difference[1], 3)
        return new_point
    else:
        raise Exception("Wrong input. Only chose 'left' or 'right' ")


def robot_mid_edge(front_pos, back_pos, side):
    # Calculate the vector representing the direction of the robot
    robot_direction = (front_pos[0] - back_pos[0], front_pos[1] - back_pos[1])

    angle_radians = math.atan2(robot_direction[1], robot_direction[0]) * -1

    point_difference = (
        (Pathfinder.robot_width() / 2) * math.sin(angle_radians),
        Pathfinder.robot_width() / 2 * math.cos(angle_radians))
    robot_center = Pathfinder.robot_center_coordinates(front_pos, back_pos)

    # HAVE TO MAKE SURE THAT "left" AND "right" ARE CORRECT WITH WHAT WAY TO TURN
    if side == "left":
        new_point = round(robot_center[0] + point_difference[0], 3), round(robot_center[1] + point_difference[1], 3)
        return new_point
    if side == "right":
        new_point = round(robot_center[0] - point_difference[0], 3), round(robot_center[1] - point_difference[1], 3)
        return new_point
    else:
        raise Exception("Wrong input. Only chose 'left' or 'right' ")


def calculate_max_left_turn(front_pos, back_pos, obstacles, side):
    smallest_angle_front, not_use = calculate_obstacle_angle(back_pos, front_pos, obstacles, side)
    smallest_angle_back, not_use2 = calculate_obstacle_angle(front_pos, back_pos, obstacles, side)
    print("front closes angle: ", smallest_angle_front)
    print("back closes angle: ", smallest_angle_back)
    if smallest_angle_front < smallest_angle_back:
        return smallest_angle_front
    if smallest_angle_back < smallest_angle_front:
        return smallest_angle_back
    else:
        print("max turn is equal left or right")
        return smallest_angle_back


def calculate_max_right_turn(front_pos, back_pos, obstacles, side):
    not_use, largest_angle_front = calculate_obstacle_angle(back_pos, front_pos, obstacles, side)
    not_use2, largest_angle_back = calculate_obstacle_angle(front_pos, back_pos, obstacles, side)
    print("front closes angle: ", largest_angle_front)
    print("back closes angle: ", largest_angle_back)
    if largest_angle_front < largest_angle_back:
        return largest_angle_front
    if largest_angle_back < largest_angle_front:
        return largest_angle_back
    else:
        print("max turn is equal left or right")
        return largest_angle_back


def max_turn(front_pos, back_pos, obstacle, side):
    if side == "left":
        max_left = calculate_max_left_turn(front_pos, back_pos, obstacle, side)
        return max_left
    if side == "right":
        max_right = calculate_max_right_turn(front_pos, back_pos, obstacles, side)
        return max_right


back_pos = (14, -4)
front_pos = (10, -8)
obstacles = [(8.69, -5.2), (14.5, -5.6), (12.5, -8.3)]
side = "right"

# edgepointmid = robot_mid_edge(front_pos, back_pos, side)
# edgepointmid2 = robot_mid_edge(back_pos, front_pos, side)
# edgepointfront = robot_front_edge(front_pos, back_pos, side)
# testangle = calculate_obstacle_angle(back_pos, front_pos, obstacles, side)
# maxangle = calculate_max_left_turn(front_pos, back_pos, obstacles, side)
maxangle2 = max_turn(front_pos, back_pos, obstacles, side)
print("max side testtesttest: ", maxangle2)
# print("new point mid ", edgepointmid)
# print("new point front: ", edgepointfront)
# print("new angle: ", testangle)
# print("smallest angle: ", maxangle)
# print("new point mid2: ", edgepointmid2)
