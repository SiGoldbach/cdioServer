import Pathfinder
import cv2
import numpy as np


def locate_center_obstacles(front_pos, back_pos, obstacles, corners):
    center_obstacles = []
    for obstacle in obstacles:
        if not Pathfinder.is_ball_near_wall(front_pos, back_pos, obstacle, corners) == "false":
            center_obstacles.append(obstacle)

    if center_obstacles:
        return center_obstacles

    raise Exception("No obstacles in center")


def create_smallest_rectangle(front_pos, back_pos, obstacles, corners):
    coordinates = locate_center_obstacles(front_pos, back_pos, obstacles, corners)
    points = np.array(coordinates)
    rect = cv2.minAreaRect(points)
    box = cv2.boxPoints(rect)
    box = np.intp(box)
    return box


def is_ball_in_center_obstacle():
    return 0

front_pos = (2, 2)
back_pos = (1, 1)
obstacles = [(20, 30), (30, 20), (40, 30), (30, 40), (10, 10), (20, 10), (20, 20), (10, 20)]
corners = [(0, 0), (100, 0), (0, 100), (100, 200)]

rectangle_corners = create_smallest_rectangle(front_pos, back_pos, obstacles, corners)
for corner in rectangle_corners:
    x, y = corner
    print("Corner X:", x)
    print("Corner Y:", y)
