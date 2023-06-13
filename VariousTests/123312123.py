import math
import Pathfinder
import numpy as np

np.set_printoptions(precision=3, suppress=True)


def calculate_obstacle_angle(back_pos, front_pos, obstacles, side):
    robot_middle = robot_mid_edge(front_pos, back_pos, side)
    robot_front = robot_front_edge(front_pos, back_pos, side)
    angles = []

    obstacles_in_range = Pathfinder.find_obstacle_in_circle(obstacles, front_pos, back_pos)

    for obstacle in obstacles_in_range:
        print("obstacles: ", obstacle)
        # Calculate the vector from the back of the robot to the obstacle
        robot_to_obstacle = (obstacle[0] - robot_middle[0], obstacle[1] - robot_middle[1])

        # Calculate the vector representing the direction of the robot
        robot_direction = (robot_front[0] - robot_middle[0], robot_front[1] - robot_middle[1])

        # Calculate the dot product of the two vectors
        dot_product = robot_to_obstacle[0] * robot_direction[0] + robot_to_obstacle[1] * robot_direction[1]

        # Calculate the magnitudes of the two vectors
        robot_to_obstacle_magnitude = math.sqrt(robot_to_obstacle[0] ** 2 + robot_to_obstacle[1] ** 2)
        robot_direction_magnitude = math.sqrt(robot_direction[0] ** 2 + robot_direction[1] ** 2)

        # Calculate the angle in radians using the arccosine function
        angle_radians = math.acos(dot_product / (robot_to_obstacle_magnitude * robot_direction_magnitude))

        # Convert the angle to degrees
        angle_degrees = math.degrees(angle_radians)

        angles.append(angle_degrees)  # Add the angle to the array

    smallest_angle = min(angles)  # Find the smallest angle in the array

    return smallest_angle, angles


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


back_pos = (5.55, 2.16)
front_pos = (11.55, 6.16)
obstacles = [(7.94, 7.52), (6.93521, 1.35819)]  # Corrected the obstacles to be a list of tuples
side = "right"

edgepointmid = robot_mid_edge(front_pos, back_pos, side)
edgepointfront = robot_front_edge(front_pos, back_pos, side)
testangle = calculate_obstacle_angle(back_pos, front_pos, obstacles, side)
print("new point mid ", edgepointmid)
print("new point front: ", edgepointfront)
print("new angle: ", testangle)
