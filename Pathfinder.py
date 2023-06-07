import math
import ImFromPhoto
import ImFromHDPhoto
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


    # print(180 - angle_degrees)
    return MoveTypes.TURN, 180 - angle_degrees


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


# def check_for_obstacle_turn(front_pos, back_pos, obstacles):
#   for obstacle in obstacles:
#      obstacle_x, obstacle_y = obstacle
#     if obstacle_x == front_pos[0] and obstacle_y == front_pos[1]:
#        return True  # collision detected with robot face
#   if obstacle_x == back_pos[0] and obstacle_y == back_pos[1]:
#      return True  # collision detected with robot ass
# return False  # no collision detected

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
    ball_locations, front, back, red_pixels = ImFromHDPhoto.imageRecognitionHD(image)
    print(red_pixels[0])
    # Temporary if statement
    if front is None or back is None:
        return Moves.MoveClass(MoveTypes.TURN, 500, 50)
    nearest_ball, distance = find_nearest_ball(front, ball_locations)
    print("This should be 2: " + str(len(front)))

    angle_to_turn = calculate_turn(front, back, nearest_ball)

    if angle_to_turn[1] > 5:
        print("I should turn: " + angle_to_turn[0])
        print(str(angle_to_turn[1]) + " degrees")
        argument = degree_to_argument(angle_to_turn[1])
        return Moves.MoveClass(angle_to_turn[0], 500, argument)


    else:
        if check_for_obstacle_front(red_pixels, nearest_ball[0], nearest_ball[1], front[0], front[1]):
            print("I am aligned and should move forward")
            return Moves.MoveClass(MoveTypes.FORWARD, 600, 600)


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
