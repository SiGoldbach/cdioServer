import math
import ImFromPhoto
import Moves
import MoveTypes


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


def calculate_line(target_x, target_y, robot_x, robot_y):
    m = ((int(target_y) - int(robot_y)) / (int(target_x) - int(robot_x)))
    b = robot_y - m * robot_x
    # vi skal parallelforskyde linjen med 16pixel hver vej. ergo b+16 | b-16
    line1 = [m, b + 25]
    line2 = [m, b - 25]
    print(line1)
    print(line2)

    return line1, line2


def check_for_obstacle(red_pixels, target_x, target_y, robot_x, robot_y):
    line1, line2 = calculate_line(target_x, target_y, robot_x, robot_y)
    red_counter = 0
    try_counter = 0

    for red_pixel in red_pixels:
        if target_x > robot_x:
            if target_x > red_pixel[0] > robot_x:
                try_counter += 1
                if check_for_red_pixel(red_pixel, line1, line2):
                    red_counter += 1
        if robot_x > target_x:
            if robot_x > red_pixel[0] > target_x:
                try_counter += 1
                if check_for_red_pixel(red_pixel, line1, line2):
                    red_counter += 1

    print("I found: " + str(red_counter) + " red pixels in the way")
    print("I tested: " + str(try_counter) + " Entries")
    return True


def check_for_red_pixel(red_pixel, line1, line2):
    x, y = red_pixel
    # Calculate the y-values for each line at the given x-coordinate
    y1 = line1[0] * x + line1[1]
    y2 = line2[0] * x + line2[1]
    # Check if the point's y-coordinate is between the y-values of the lines
    if min(y1, y2) <= y <= max(y1, y2):
        return True
    else:
        return False


# This function is being written iteratively.
# Meaning only moves which we have a realistic chance of taking are added to the control flow
# At current time:
# The robot can turn and align itself to a ball
# It can move forward if is aligned
def make_move(image):
    print("Now doing image recognition")
    ball_locations, front, back, red_pixels = ImFromPhoto.imageRecognition(image)
    print(red_pixels[0])
    # Temporary if statement
    if front is None or back is None:
        return Moves.MoveClass(MoveTypes.LEFT, 500, 50)
    nearest_ball, distance = find_nearest_ball(front, ball_locations)
    print("This should be 2: " + str(len(front)))

    # fictive goal location for this purpose. Need information from img-recognation
    #  goal_location = [0, 0]
    # angle_to_goal = calculate_turn(front, back, goal_location)

    # if len(ball_locations) == 0 & angle_to_goal[1] > 5:
    #    print("i should turn to goal: " + angle_to_goal[0])
    #   print(str(angle_to_goal[1]) + " degrees")
    #  argument = degree_to_argument(angle_to_goal[1])
    # return Moves.MoveClass(angle_to_goal[0], 500, argument)

    #   if len(ball_locations) == 0 & angle_to_goal[1] < 5:
    #      if check_for_obstacle(red_pixels, nearest_ball[0], nearest_ball[1], front[0], front[1]):
    #         print("I am aligned with the goal and should move forward")
    #        return Moves.MoveClass(MoveTypes.FORWARD, 600, 600)

    angle_to_turn = calculate_turn(front, back, nearest_ball)

    if angle_to_turn[1] > 5:
        print("I should turn: " + angle_to_turn[0])
        print(str(angle_to_turn[1]) + " degrees")
        argument = degree_to_argument(angle_to_turn[1])
        return Moves.MoveClass(angle_to_turn[0], 500, argument)


    else:
        if check_for_obstacle(red_pixels, nearest_ball[0], nearest_ball[1], front[0], front[1]):
            print("I am aligned and should move forward")
            return Moves.MoveClass(MoveTypes.FORWARD, 600, 600)
