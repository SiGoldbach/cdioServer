import math
import Moves
import MoveTypes
import detectRobot
import robot_modes

ROBOT_WIDTH = 2
DISTANCE_FROM_WALL = 30
CALCULATE_LINE_WIDTH = 25
DISTANCE_TO_GOAL = 40
BALL_TO_WALL = 30

DIRECTION_TOP = "top"
DIRECTION_BOTTOM = "bottom"
DIRECTION_LEFT = "left"
DIRECTION_RIGHT = "right"
DIRECTION_NOT_NEAR = "false"


def get_robot_length(front_pos, back_pos):
    robot_length = math.sqrt((front_pos[0] - back_pos[0]) ** 2 + (front_pos[1] - back_pos[1]) ** 2)
    return robot_length


def distance_to_point(current_location, goal_location):
    distance = math.sqrt((int(current_location[0]) - int(goal_location[0])) ** 2 + int(
        (current_location[1]) - int(goal_location[1])) ** 2)
    return distance


def robot_center_coordinates(front_pos, back_pos):
    robot_center = (int(front_pos[0]) + int(back_pos[0])) / 2, (int(front_pos[1]) + int(back_pos[1])) / 2
    return robot_center


# Width of the robot
def robot_width():
    width = 2
    return width


# Center of the field
def center_field(corners):
    minX = min(corners[0][0], corners[1][0], corners[2][0], corners[3][0])
    maxX = max(corners[0][0], corners[1][0], corners[2][0], corners[3][0])
    minY = min(corners[0][1], corners[1][1], corners[2][1], corners[3][1])
    maxY = max(corners[0][1], corners[1][1], corners[2][1], corners[3][1])
    print("HELLO", maxX + minX, maxY + minY)
    field_center = [((maxX + minX) / 2, (maxY + minY) / 2)]
    return field_center


# Location of a given goal
import numpy as np


# Remade with numpy array
def big_goal_location(corners):
    corners = np.array(corners)
    maxX = np.max(corners[:, 0])
    maxY = np.max(corners[:, 1])
    minY = np.min(corners[:, 1])
    goal = [maxX, (maxY + minY) / 2]
    return goal


# Remade with numpy array
def small_goal_location(corners):
    corners = np.array(corners)
    minX = np.min(corners[:, 0])
    maxY = np.max(corners[:, 1])
    minY = np.min(corners[:, 1])
    goal = [minX, (maxY + minY) / 2]
    return goal


# def big_goal_location(corners):
#     maxX = max(corners[0][0], corners[1][0], corners[2][0], corners[3][0])
#     maxY = max(corners[0][1], corners[1][1], corners[2][1], corners[3][1])
#     minY = min(corners[0][1], corners[1][1], corners[2][1], corners[3][1])
#     goal = [maxX, (maxY + minY) / 2]
#     return goal
#
#
# def small_goal_location(corners):
#     minX = min(corners[0][0], corners[1][0], corners[2][0], corners[3][0])
#     maxY = max(corners[0][1], corners[1][1], corners[2][1], corners[3][1])
#     minY = min(corners[0][1], corners[1][1], corners[2][1], corners[3][1])
#     goal = [minX, (maxY + minY) / 2]
#     return goal


def robot_corner_radius(front_pos, back_pos):
    robot_center = robot_center_coordinates(front_pos, back_pos)
    x_center = robot_center[0]
    y_center = robot_center[1]
    robot_radius = math.sqrt((front_pos[0] - x_center) ** 2 + (front_pos[1] - y_center) ** 2)
    radius = math.sqrt(robot_radius ** 2 + robot_width() ** 2)
    return radius


def find_nearest_ball(front_pos, ball_locations):
    closest_distance = float('inf')
    closest_coordinate = []
    r1 = int(front_pos[0])
    r2 = int(front_pos[1])

    for coordinate in ball_locations:
        x = int(coordinate[0])
        y = int(coordinate[1])
        distance = math.sqrt((x - r1) ** 2 + (y - r2) ** 2)

        if distance < closest_distance:
            closest_distance = distance
            closest_coordinate = coordinate

    return closest_coordinate, closest_distance


# This function finds the angle between the two vector that are ass to ball and ass to head
# This goes from left to right if the value is negative the robot is to the right.
def calculate_turn(back_pos, front_pos, ball_pos):
    # Calculate the vector from the front to the back of the robot
    # MIGHT HAVE TO CHANGE "front" AND "back"
    robot_vector = (int(front_pos[0]) - int(back_pos[0]), int(front_pos[1]) - int(back_pos[1]))

    # Calculate the vector from the front of the robot to the target position
    target_vector = (int(ball_pos[0]) - int(back_pos[0]), int(ball_pos[1]) - int(back_pos[1]))

    # Calculate the signed angle between the robot vector and the target vector
    angle_radians = math.atan2(target_vector[1], target_vector[0]) - math.atan2(robot_vector[1], robot_vector[0])
    angle_degrees = math.degrees(angle_radians)

    if angle_degrees < -180:
        angle_degrees += 360
    if angle_degrees > 180:
        angle_degrees -= 360

    return angle_degrees


def calculate_drive_distance(distance):
    return distance * 2


def calculate_line(target_x, target_y, robot_x, robot_y):
    m = ((int(target_y) - int(robot_y)) / (int(target_x) - int(robot_x)))
    b = robot_y - m * robot_x
    # y = m * x + b
    # vi skal parallelforskyde linjen med 25pixel hver vej. ergo b+25 | b-25
    line1 = [m, b + CALCULATE_LINE_WIDTH]
    line2 = [m, b - CALCULATE_LINE_WIDTH]
    print(line1)
    print(line2)
    return line1, line2


# Checks for obstacles between ball and robot.
def check_for_obstacle_location(obstacles, line1, line2):
    x, y = obstacles
    # Calculate the y-values for each line at the given x-coordinate
    y1 = line1[0] * x + line1[1]
    y2 = line2[0] * x + line2[1]
    # Check if the point's y-coordinate is between the y-values of the lines
    if min(y1, y2) <= y <= max(y1, y2):
        return True
    else:
        return False


# Method for checking how many obstacles are located in the area in front of the robot between it and the ball.
def check_for_obstacle_front(obstacles, target_x, target_y, robot_x, robot_y):
    line1, line2 = calculate_line(target_x, target_y, robot_x, robot_y)
    # method scanning for obstacles.
    obstacle_counter = 0
    try_counter = 0
    for obstacle in obstacles:
        if target_x > robot_x:
            if target_x > obstacle[0] > robot_x:
                try_counter += 1
                if check_for_obstacle_location(obstacle, line1, line2):
                    obstacle_counter += 1
            if robot_x > target_x:
                if robot_x > obstacle[0] > target_x:
                    try_counter += 1
                if check_for_obstacle_location(obstacle, line1, line2):
                    obstacle_counter += 1

    print("I found: " + str(obstacle_counter) + " obstacles in the way")
    print("I tested: " + str(try_counter) + " Entries")
    return True


# SHOULD find if an obstacle is within turn-range of the robot.
def find_obstacle_in_circle(obstacles, front_pos, back_pos):
    robot_center = robot_center_coordinates(front_pos, back_pos)
    robot_radius = robot_corner_radius(front_pos, back_pos)
    obstacles_in_range = []
    for obstacle in obstacles:
        x, y = obstacle
        obstacle_distance = math.sqrt((x - robot_center[0]) ** 2 + (y - robot_center[1]) ** 2)
        if obstacle_distance <= robot_radius:
            obstacles_in_range.append(obstacle)
    return obstacles_in_range


# Checking if robot is in the within the corners to make sure robot never hits walls. Only works if
# we get the corners as a single location and not an array of multiple coordinates.
def check_borders(corners, front_pos, back_pos):
    # here we can hard-code minimum distance "buffer" to the walls.
    minX = min(corners[0][0], corners[1][0], corners[2][0], corners[3][0])
    maxX = max(corners[0][0], corners[1][0], corners[2][0], corners[3][0])
    minY = min(corners[0][1], corners[1][1], corners[2][1], corners[3][1])
    maxY = max(corners[0][1], corners[1][1], corners[2][1], corners[3][1])
    # check if the robot back or front's x-coordinate is
    if front_pos[0] <= minX or back_pos[0] <= minX:
        # Robot is hitting the left border, take appropriate action here
        print("Robot hit the left border!")
    elif front_pos[0] >= maxX or back_pos[0] >= maxX:
        # Robot is hitting the right border, take appropriate action here
        print("Robot hit the right border!")
    elif front_pos[1] <= minY or back_pos[1] <= minY:
        # Robot is hitting the bottom border, take appropriate action here
        print("Robot hit the bottom border!")
    elif front_pos[1] >= maxY or back_pos[1] >= maxY:
        # Robot is hitting the top border, take appropriate action here
        print("Robot hit the top border!")
    return minX, maxX, minY, maxY


# This function is being written iteratively.
# Meaning only moves which we have a realistic chance of taking are added to the control flow
# At current time:
# The robot can turn and align itself to a ball
# It can move forward if is aligned
# Change has been added to this function so it is now a collect balls method
def collect_balls(state):
    front_pos, back = detectRobot.detect_robot()
    if state.goal_ball is None:
        nearest_ball, distance_to_nearest_ball = find_nearest_ball(front_pos, state.balls)
        state.goal_ball = nearest_ball
    distance_to_goal_ball = distance_to_point(front_pos, state.goal_ball)

    print("Back: ", str(back))
    print("Front: ", str(front_pos))
    print("Closest ball: ", str(state.goal_ball))

    angle_to_turn = calculate_turn(back_pos=robot_center_coordinates(front_pos, back), front_pos=front_pos,
                                   ball_pos=state.goal_ball)
    print(angle_to_turn)

    if angle_to_turn > 5 or angle_to_turn < -5:
        print("I should turn: " + str(angle_to_turn))
        print(str(angle_to_turn) + " degrees")
        return Moves.MoveClass(MoveTypes.TURN, 500, angle_to_turn)
    else:
        if distance_to_goal_ball > 300:
            return Moves.MoveClass(MoveTypes.FORWARD, 500, distance_to_goal_ball / 2)
        else:
            state.goal_ball = None
            state.need_new_detect_balls = True
            state.ball_amount_guess = state.ball_amount_guess + 1
            if state.ball_amount_guess == 5:
                state.mode = robot_modes.DELIVER
                state.ball_amount_guess = 0
            return Moves.MoveClass(MoveTypes.FORWARD, 500, calculate_drive_distance(distance_to_goal_ball) + 30)


def move_to_goal(state, goal, offset):
    # I am getting the robots location from image recognition
    front_pos, back_pos = detectRobot.detect_robot()

    # First i am checking if the robot is at the goal already
    if state.delivery_mode == robot_modes.AT_GOAL:
        return deliver(front_pos, back_pos, state, goal)

    robot_middle = robot_center_coordinates(front_pos, back_pos)
    distance_from_offset_to_middle = distance_to_point(robot_middle, offset)
    if distance_from_offset_to_middle < 40 or state.delivery_mode == robot_modes.AT_CHECKPOINT:
        state.delivery_mode = robot_modes.AT_CHECKPOINT
        return drive_back_to_goal(front_pos, back_pos, state, goal)
    # The robot is not at the offset and has never been meaning it should drive there
    angle_to_turn = calculate_turn(front_pos, back_pos, offset)
    if angle_to_turn > 5 or angle_to_turn < -5:
        print("I should turn: " + str(angle_to_turn))
        print(str(angle_to_turn) + " degrees")
        return Moves.MoveClass(MoveTypes.TURN, 500, int(angle_to_turn))
    else:
        distance = distance_to_point(back_pos, offset)
        return Moves.MoveClass(MoveTypes.FORWARD, 500, -calculate_drive_distance(distance))


def drive_back_to_goal(front_pos, back_pos, state, goal):
    print("I will align my butt to the goal")
    front_angle_to_goal = calculate_turn(front_pos, back_pos, goal)
    if 3 > front_angle_to_goal > -3:
        print("I am aligned to the goal")
        drive_distance = distance_to_point(back_pos, goal)
        state.delivery_mode = robot_modes.AT_GOAL
        return Moves.MoveClass(MoveTypes.FORWARD, 500, -(calculate_drive_distance(drive_distance) - 80))
    else:
        return Moves.MoveClass(MoveTypes.TURN, 500, front_angle_to_goal)


def deliver(front_pos, back_pos, state, goal):
    # Here I am calculating the angle reverse of usual because the back needs to line up instead of the front
    angle_to_goal = calculate_turn(front_pos, back_pos, goal)
    if 3 > angle_to_goal > -3:
        # Now the robot will deliver the balls and go back to collect mode and reset is delivery_mode
        state.mode = robot_modes.COLLECT
        state.delivery_mode = robot_modes.AT_RANDOM_PLACE
        return Moves.MoveClass(MoveTypes.DELIVER, 0, 0)
    else:
        return Moves.MoveClass(MoveTypes.TURN, 500, angle_to_goal)


def deliver_balls(state):
    # From the state I am now making 2 points the goal and the offset point the robot should drive to
    goal, offset = None, None
    if state.big_or_small_goal == robot_modes.BIG_GOAL:
        print("I will deliver in the large goal")
        goal = state.large_goal
        offset = state.robot_delivery_location_big
    if state.big_or_small_goal == robot_modes.SMALL_GOAL:
        goal = state.small_goal
        offset = state.robot_delivery_location_small

    # This method is figuring out what the robot should do with a given goal and offset

    return move_to_goal(state, goal, offset)


def calculate_obstacle_angle(back_pos, front_pos, obstacles, side):
    robot_middle = robot_mid_edge(front_pos, back_pos, side)
    robot_front = robot_front_edge(front_pos, back_pos, side)
    angles = []
    if not find_obstacle_in_circle(obstacles, front_pos, back_pos):
        angles.append(180)

    for obstacle in find_obstacle_in_circle(obstacles, front_pos, back_pos):
        angle = getAngle(robot_front, robot_middle, obstacle)
        if side == "left":
            if angle > 0:
                angles.append(angle)  # Add the angle to the array
            if angle < 0:
                angle = 360 - (angle * -1)
                angles.append(angle)

        if side == "right":

            if angle > 180:
                angle = 360 - angle
                angles.append(angle)
            elif angle < 0:
                angle = angle * -1
                angles.append(angle)
            else:
                angle = 500
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
        (robot_width() / 2) * math.sin(angle_radians),
        robot_width() / 2 * math.cos(angle_radians))
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
        (robot_width() / 2) * math.sin(angle_radians),
        robot_width() / 2 * math.cos(angle_radians))
    robot_center = robot_center_coordinates(front_pos, back_pos)

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
    smallest_angle_front, not_use = calculate_obstacle_angle(back_pos, front_pos, obstacles, side)
    smallest_angle_back, not_use2 = calculate_obstacle_angle(front_pos, back_pos, obstacles, side)
    print("front closes angle: ", smallest_angle_front)
    print("back closes angle: ", smallest_angle_back)
    return min(smallest_angle_front, smallest_angle_back)


# Finds the max turn if any obstacle is within range
def max_turn(front_pos, back_pos, obstacles, side):
    if side == "left":
        max_left = calculate_max_left_turn(front_pos, back_pos, obstacles, side)
        return max_left
    if side == "right":
        max_right = calculate_max_right_turn(front_pos, back_pos, obstacles, side)
        return max_right


# The method to pick up ball near wall
def move_to_wall_ball(front_pos, back_pos, ball_location, corners):
    front_pos1 = robot_center_coordinates(front_pos, back_pos)
    distance_to_ball = distance_to_point(front_pos, ball_location)
    if wall_robot_align(front_pos1, back_pos, ball_location, corners):
        return Moves.MoveClass(MoveTypes.FORWARD, 500, distance_to_ball)
    else:
        raise Exception("Something went wrong in move_to_wall_ball method or its calculations")


# To make sure the robot is aligned with the ball either horizontally or vertically depending on ball location
def wall_robot_align(front_pos, back_pos, ball_location, corners):
    robot_center = robot_center_coordinates(front_pos, back_pos)
    direction = is_ball_near_wall(front_pos, back_pos, ball_location, corners)
    turn_align_ball = calculate_turn(back_pos, front_pos, ball_location)

    if direction == DIRECTION_LEFT or direction == DIRECTION_RIGHT:
        if robot_center[1] <= ball_location[1] - 10 or robot_center[1] >= ball_location[1] + 10:
            turn_pos = (robot_center[0], ball_location[1])
            turn_align_pos = calculate_turn(back_pos, front_pos, turn_pos)
            dist_pos_align = distance_to_point(front_pos, turn_pos)
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
            turn_align_pos = calculate_turn(back_pos, front_pos, turn_pos)
            dist_pos_align = distance_to_point(front_pos, turn_pos)
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
    minX, maxX, minY, maxY = check_borders(corners, front_pos, back_pos)
    # Hardcoded a pixel-difference. May need change
    if ball_location[0] <= minX + DISTANCE_FROM_WALL and ball_location[1] >= minY + DISTANCE_FROM_WALL & ball_location[
        1] <= maxY - DISTANCE_FROM_WALL:
        direction = DIRECTION_LEFT
        print(direction)
        return direction
    if ball_location[0] >= maxX - DISTANCE_FROM_WALL and ball_location[1] >= minY + DISTANCE_FROM_WALL & ball_location[
        1] <= maxY - DISTANCE_FROM_WALL:
        direction = DIRECTION_RIGHT
        print(direction)
        return direction
    if ball_location[1] <= minY + DISTANCE_FROM_WALL and minX + DISTANCE_FROM_WALL <= ball_location[
        0] <= maxX - DISTANCE_FROM_WALL:
        direction = DIRECTION_TOP
        print(direction)
        return direction
    if ball_location[1] >= maxY - DISTANCE_FROM_WALL and minX + DISTANCE_FROM_WALL <= ball_location[
        0] <= maxX - DISTANCE_FROM_WALL:
        direction = DIRECTION_BOTTOM
        print(direction)
        return direction
    else:
        print("Ball is not near wall")
        return DIRECTION_NOT_NEAR


def is_ball_near_corner(balls, corners):
    for ball in balls:
        for corner in corners:
            if distance_to_point(ball, corner) < 30:
                return True, ball, corner

    return False
