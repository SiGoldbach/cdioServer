import math

import Moves
import MoveTypes
import detectRobotAndBalls


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

    # print(180 - angle_degrees)

    return MoveTypes.TURN, angle_degrees


# Method for calculating angle has been updated based on the quadrant and should now work in most cases
def angle_good(p1, head1, ball1):
    m1 = (head1[1] - p1[1]) / (head1[0] - p1[0])
    m2 = (ball1[1] - p1[1]) / (ball1[0] - p1[0])

    angle_cal = math.atan((m2 - m1) / (1 + m1 * m2)) * 180 / math.pi

    # Adjust the angle based on the quadrant
    if head1[0] - p1[0] < 0:
        angle_cal += 180
    elif ball1[0] - p1[0] < 0:
        angle_cal += 180

    return angle_cal


def degree_to_argument(degrees):
    print("Calculating argument ")
    argumentTurn = (degrees - -5.862845) / 0.209388
    return int(argumentTurn) / 2


def calculate_line(target_x, target_y, robot_x, robot_y):
    m = ((int(target_y) - int(robot_y)) / (int(target_x) - int(robot_x)))
    b = robot_y - m * robot_x
    # y = m * x + b
    # vi skal parallelforskyde linjen med 25pixel hver vej. ergo b+25 | b-25
    line1 = [m, b + 25]
    line2 = [m, b - 25]
    print(line1)
    print(line2)
    return line1, line2


def check_for_max_turn(obstacles, front_pos, back_pos):
    x, y = obstacles
    robot_length = math.sqrt((front_pos[0] - back_pos[0]) ^ 2 + (front_pos[1] - back_pos[1]) ^ 2)
    radius = robot_length / 2
    obstacle_distance = math.sqrt((front_pos[0] - obstacles[0]) ^ 2 + (front_pos[1] - obstacles[1]) ^ 2)
    outside_counter = 0
    inside_counter = 0
    for obstacle in obstacles:
        if obstacle_distance > radius:
            outside_counter += 1
        if obstacle_distance < radius:
            inside_counter += 1

    max_turn_left = 0
    max_turn_right = 0


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


def check_borders(corners, front_pos, back_pos):
    # here we can hard-code minimum distance "buffer" to the walls.
    minX = corners[0][0]
    maxX = corners[1][0]
    minY = corners[2][1]
    maxY = corners[3][1]

    # check if the robot back or front's x-coordinate is
    if front_pos[0] <= minX or back_pos[0] <= minX:
        # Robot is hitting the left border
        # Take appropriate action here
        print("Robot hit the left border!")
    elif front_pos[0] >= maxX or back_pos[0] >= maxX:
        # Robot is hitting the right border
        # Take appropriate action here
        print("Robot hit the right border!")
    elif front_pos[1] <= minY or back_pos[1] <= minY:
        # Robot is hitting the bottom border
        # Take appropriate action here
        print("Robot hit the bottom border!")
    elif front_pos[1] >= maxY or back_pos[1] >= maxY:
        # Robot is hitting the top border
        # Take appropriate action here
        print("Robot hit the top border!")


# This function is being written iteratively.
# Meaning only moves which we have a realistic chance of taking are added to the control flow
# At current time:
# The robot can turn and align itself to a ball
# It can move forward if is aligned
def make_move(image):
    print("Now doing image recognition")
    front, back, balls = detectRobotAndBalls.imageRecognitionHD(image)
    # Temporary if statement
    if front is None or back is None:
        return Moves.MoveClass(MoveTypes.TURN, 500, 50)
    nearest_ball, distance = find_nearest_ball(front, balls)
    print("Back is: " + str(back))
    print("Front is: " + str(front))
    print("Closest ball is: " + str(nearest_ball))

    angle_to_turn = angle_good(back, front, nearest_ball)
    print(angle_to_turn)

    if angle_to_turn > 5 or angle_to_turn < -5:
        print("I should turn: " + str(angle_to_turn))
        print(str(angle_to_turn) + " degrees")
        return Moves.MoveClass(MoveTypes.TURN, 500, angle_to_turn)
    else:
        return Moves.MoveClass(MoveTypes.FORWARD, 500, 1000)


def drive_to_goal(ball_locations, front_pos, back_pos, center_of_field):
    # fictive goal location for this purpose. Need information from img-recognation
    center_of_field = [10, 10]
    # fictive goal location
    goal_location = [3, 3]

    robot_mid_location = (int(back_pos[0]) + int(front_pos[0]) / 2, int(back_pos[1]) + int(front_pos[1]) / 2)
    align_robot_goal = [robot_mid_location[0], center_of_field[1]]
    angle_to_turn_y = calculate_turn(front_pos, back_pos, align_robot_goal)
    drive_distance = math.sqrt(
        (align_robot_goal[0] - robot_mid_location[0]) ** 2 + (align_robot_goal[1] - robot_mid_location[1]) ** 2)
    argument_turn = degree_to_argument(angle_to_turn_y[1])
    # need goal location x and y coordinates.
    angle_to_goal = calculate_turn(front_pos, back_pos, goal_location)

    if angle_to_turn_y[1] > 6 & len(ball_locations) == 0:
        print("i should move to center y: " + angle_to_turn_y[0])
        print(str(angle_to_turn_y[1]) + " degrees")
        # need to find distance moved for argument
        return Moves.MoveClass(angle_to_turn_y[0], 500, argument_turn)

    if angle_to_turn_y[1] <= 6:
        # if the angle to turn is so low, that we are already on track for the correct y-axis,
        # and the distance to drive is so small we assume we are on the desired x,y spot.
        if drive_distance < 5:
            print("I should turn: " + angle_to_goal[0])
            print(str(angle_to_goal[1]) + " degrees")
            argument = degree_to_argument(angle_to_goal[1])
            return Moves.MoveClass(angle_to_goal[0], 500, -argument)
            # here we have to turn with ass against small goal and reverse there

    return Moves.MoveClass(MoveTypes.FORWARD, 600, drive_distance)
