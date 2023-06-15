import math
import MoveTypes
import Pathfinder
from Moves import MoveClass
import detectBalls
import detectField
import detectRobot


def collection_of_wall_balls(front_pos, back_pos, obstacles, ball_locations, corners):
    front_pos = Pathfinder.robot_center_coordinates(front_pos, back_pos)
    is_safe = Pathfinder.check_borders(corners, front_pos, back_pos)

    return 0


def wall_ball_align(front_pos, back_pos, ball_locations, corners):
    robot_mid = Pathfinder.robot_center_coordinates(front_pos, back_pos)
    isTrue, direction = is_ball_near_wall(front_pos, back_pos, ball_locations, corners)
    if isTrue:
        if direction == "left":

            return 0
    else:
        print("Ball is not near wall")
        return False


def is_ball_near_wall(front_pos, back_pos, ball_location, corners):
    minX, maxX, minY, maxY = Pathfinder.check_borders(corners, front_pos, back_pos)
    # Hardcoded a pixel-difference. May need change
    if ball_location[0] - 20 <= minX and ball_location[1] + 20 >= minY and ball_location[1] - 20 <= maxY:
        direction = "left"
        return True, direction
    if ball_location[0] + 20 >= maxX and ball_location[1] + 20 >= minY and ball_location[1] - 20 <= maxY:
        direction = "right"
        return True, direction
    if ball_location[1] - 20 <= minY and ball_location[0] + 20 >= minX and ball_location[0] - 20 <= maxX:
        direction = "top"
        return True, direction
    if ball_location[1] + 20 >= maxY and ball_location[0] + 20 >= minX and ball_location[0] - 20 <= maxX:
        direction = "down"
        return True, direction
    else:
        print("Ball is not near wall")
        return False, "false"
