import math
import MoveTypes
import Moves
import Pathfinder
from Moves import MoveClass
import detectBalls
import detectField
import detectRobot


# The
def move_to_wall_ball(front_pos, back_pos, ball_location, corners):
    front_pos1 = Pathfinder.robot_center_coordinates(front_pos, back_pos)
    distance_to_ball = Pathfinder.distance_to_ball(front_pos, ball_location)
    if wall_robot_align(front_pos1, back_pos, ball_location, corners):
        return Moves.MoveClass(MoveTypes.FORWARD, 500, distance_to_ball)
    else:
        raise Exception("Something went wrong in move_to_wall_ball method or its calculations")


# To make sure the robot is aligned with the ball either horizontally or vertically depending on ball location
def wall_robot_align(front_pos, back_pos, ball_location, corners):
    robot_center = Pathfinder.robot_center_coordinates(front_pos, back_pos)
    isTrue, direction = is_ball_near_wall(front_pos, back_pos, ball_location, corners)
    turn_align_ball = Pathfinder.calculate_turn(back_pos, front_pos, ball_location)

    if isTrue:
        if direction == "left" or "right":
            if robot_center[1] <= ball_location[1] - 10 or robot_center[1] >= ball_location[1] + 10:
                turn_pos = (robot_center[0], ball_location[1])
                turn_align_pos = Pathfinder.calculate_turn(back_pos, front_pos, turn_pos)
                dist_pos_align = Pathfinder.distance_to_ball(front_pos, turn_pos)
                if turn_align_pos <= 5 or turn_align_pos >= -5:
                    return Moves.MoveClass(MoveTypes.TURN, 500, turn_align_pos)
                if turn_align_pos < 5 or turn_align_pos > -5:
                    return Moves.MoveClass(MoveTypes.FORWARD, 500, dist_pos_align)
                if turn_align_ball <= 5 or turn_align_ball >= -5:
                    return Moves.MoveClass(MoveTypes.TURN, 500, turn_align_ball)

            if direction == "top" or direction == "down":
                if robot_center[0] <= ball_location[0] - 10 or robot_center[0] >= ball_location[0] + 10:
                    turn_pos = (robot_center[1], ball_location[0])
                    turn_align_pos = Pathfinder.calculate_turn(back_pos, front_pos, turn_pos)
                    dist_pos_align = Pathfinder.distance_to_ball(front_pos, turn_pos)
                if turn_align_pos <= 5 or turn_align_pos >= -5:
                    return Moves.MoveClass(MoveTypes.TURN, 500, turn_align_pos)
                if turn_align_pos < 5 or turn_align_pos > -5:
                    return Moves.MoveClass(MoveTypes.FORWARD, 500, dist_pos_align)
                if turn_align_ball <= 5 or turn_align_ball >= -5:
                    return Moves.MoveClass(MoveTypes.TURN, 500, turn_align_ball)
    else:
        return True


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


front_pos = (100, 200)
back_pos = (50, 250)
obstacles = [(150, 150), (200, 200)]
ball_location = (280, 160)
corners = [(0, 0), (300, 0), (300, 300), (0, 300)]
test123 = move_to_wall_ball(front_pos, back_pos, ball_location, corners)
print(test123)
