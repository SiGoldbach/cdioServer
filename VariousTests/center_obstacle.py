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
    print("box: ", box)
    return box


def is_ball_in_center_obstacle(rectangle_corners, ball_location):
    rect_center, rect_size, rect_angle = cv2.minAreaRect(rectangle_corners)

    min_x = min(rectangle_corners[:, 0])
    max_x = max(rectangle_corners[:, 0])
    min_y = min(rectangle_corners[:, 1])
    max_y = max(rectangle_corners[:, 1])
    print("min_x:", min_x, "max_x:", max_x, "min_y:", min_y, "max_y:", max_y)

    # Calculate the rotation matrix based on the angle
    rotation_matrix = cv2.getRotationMatrix2D(rect_center, rect_angle, scale=1.0)
    rotation_matrix = rotation_matrix.reshape(1, 2, 3)  # Reshape the rotation matrix

    # Transform the ball_location based on the rotation matrix
    transformed_ball_location = cv2.transform(np.array([ball_location]), rotation_matrix)[0]

    if min_x <= transformed_ball_location[0] <= max_x and min_y <= transformed_ball_location[1] <= max_y:
        return True
    else:
        return False




front_pos = (2, 2)
back_pos = (1, 1)
obstacles = [(20, 30), (30, 20), (40, 30), (30, 40), (10, 10), (20, 10), (20, 20), (10, 20)]
corners = [(0, 0), (100, 0), (0, 100), (100, 200)]
ball_location = [30, 20]

rectangle_corners = create_smallest_rectangle(front_pos, back_pos, obstacles, corners)

if is_ball_in_center_obstacle(rectangle_corners, ball_location):
    print("Ball is within the rectangle.")
else:
    print("Ball is not within the rectangle.")
