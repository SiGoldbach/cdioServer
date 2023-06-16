import MoveTypes
import Moves
import Pathfinder

DIRECTION_TOP = "top"
DIRECTION_BOTTOM = "bottom"
DIRECTION_LEFT = "left"
DIRECTION_RIGHT = "right"
DIRECTION_NOT_NEAR = "false"


# The method to pick up ball near wall
def move_to_wall_ball(front_pos, back_pos, ball_location, corners):
    front_pos1 = Pathfinder.robot_center_coordinates(front_pos, back_pos)
    distance_to_ball = Pathfinder.distance_to_point(front_pos, ball_location)
    if wall_robot_align(front_pos1, back_pos, ball_location, corners):
        return Moves.MoveClass(MoveTypes.FORWARD, 500, distance_to_ball)
    else:
        raise Exception("Something went wrong in move_to_wall_ball method or its calculations")


# To make sure the robot is aligned with the ball either horizontally or vertically depending on ball location
def wall_robot_align(front_pos, back_pos, ball_location, corners):
    robot_center = Pathfinder.robot_center_coordinates(front_pos, back_pos)
    direction = is_ball_near_wall(front_pos, back_pos, ball_location, corners)
    turn_align_ball = Pathfinder.calculate_turn(back_pos, front_pos, ball_location)

    if direction == DIRECTION_LEFT or direction == DIRECTION_RIGHT:
        if robot_center[1] <= ball_location[1] - 10 or robot_center[1] >= ball_location[1] + 10:
            turn_pos = (robot_center[0], ball_location[1])
            turn_align_pos = Pathfinder.calculate_turn(back_pos, front_pos, turn_pos)
            dist_pos_align = Pathfinder.distance_to_point(front_pos, turn_pos)
            if turn_align_pos <= 5 or turn_align_pos >= -5:
                return Moves.MoveClass(MoveTypes.TURN, 500, turn_align_pos)
            print("i have to turn: ", turn_align_pos)
            if turn_align_pos < 5 or turn_align_pos > -5:
                print("i have to move: ", dist_pos_align)
                return Moves.MoveClass(MoveTypes.FORWARD, 500, dist_pos_align)
            if turn_align_ball <= 5 or turn_align_ball >= -5:
                print("i have to turn: ", turn_align_ball)
                return Moves.MoveClass(MoveTypes.TURN, 500, turn_align_ball)

    if direction == DIRECTION_TOP or direction == DIRECTION_BOTTOM:
        if robot_center[0] <= ball_location[0] - 10 or robot_center[0] >= ball_location[0] + 10:
            turn_pos = (robot_center[1], ball_location[0])
            turn_align_pos = Pathfinder.calculate_turn(back_pos, front_pos, turn_pos)
            dist_pos_align = Pathfinder.distance_to_point(front_pos, turn_pos)
            if turn_align_pos <= 5 or turn_align_pos >= -5:
                print("i have to turn: ", turn_align_pos)
                return Moves.MoveClass(MoveTypes.TURN, 500, turn_align_pos)
            if 5 > turn_align_pos > -5:
                print("i have to move: ", dist_pos_align)
                return Moves.MoveClass(MoveTypes.FORWARD, 500, dist_pos_align)
            if turn_align_ball <= 5 or turn_align_ball >= -5:
                print("i have to turn: ", turn_align_ball)
                return Moves.MoveClass(MoveTypes.TURN, 500, turn_align_ball)
    else:
        print("no need for alignment")
        return True


def is_ball_near_wall(front_pos, back_pos, ball_location, corners):
    minX, maxX, minY, maxY = Pathfinder.check_borders(corners, front_pos, back_pos)
    # Hardcoded a pixel-difference. May need change
    if ball_location[0] <= minX + 30 and ball_location[1] >= minY + 30 & ball_location[1] <= maxY - 30:
        direction = DIRECTION_LEFT
        print(direction)
        return direction
    if ball_location[0] >= maxX - 30 and ball_location[1] >= minY + 30 & ball_location[1] <= maxY - 30:
        direction = DIRECTION_RIGHT
        print(direction)
        return direction
    if ball_location[1] <= minY + 30 and minX + 30 <= ball_location[0] <= maxX - 30:
        direction = DIRECTION_TOP
        print(direction)
        return direction
    if ball_location[1] >= maxY - 30 and minX + 30 <= ball_location[0] <= maxX - 30:
        direction = DIRECTION_BOTTOM
        print(direction)
        return direction
    else:
        print("Ball is not near wall")
        return DIRECTION_NOT_NEAR


front_pos = (906, 140)
back_pos = (874, 246)
obstacles = [(150, 150), (200, 200)]

corners = [(1046, 609), (1035, 45), (279, 599), (272, 93)]
minX, maxX, minY, maxY = Pathfinder.check_borders(corners, front_pos, back_pos)
print("minX: ", minX, "maxX: ", maxX, "minY: ", minY, "maxY: ", maxY)
ball_location = (1020, 242)
print("ball location: ", ball_location)
test123 = move_to_wall_ball(front_pos, back_pos, ball_location, corners)
print(test123.argument)
