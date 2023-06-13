import math
import Moves
import MoveTypes
import detectField
import detectRobotAndBalls


def get_robot_length(front_pos, back_pos):
    robot_length = math.sqrt((front_pos[0] - back_pos[0]) ** 2 + (front_pos[1] - back_pos[1]) ** 2)
    return robot_length


def robot_center_coordinates(front_pos, back_pos):
    robot_center = (front_pos[0] + back_pos[0]) / 2, (front_pos[1] + back_pos[1]) / 2
    return robot_center


def robot_width():
    width = 2
    return width


def robot_corner_radius(front_pos, back_pos):
    robot_center = robot_center_coordinates(front_pos, back_pos)
    x_center = robot_center[0]
    y_center = robot_center[1]
    robot_radius = math.sqrt((front_pos[0] - x_center) ** 2 + (front_pos[1] - y_center) ** 2)
    radius = math.sqrt(robot_radius ** 2 + robot_width() ** 2)
    return radius


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
# This goes from left to right if the value is negative the robot is to the right.
def calculate_turn(back, front, ball):
    # Calculate the vector from the front to the back of the robot
    # MIGHT HAVE TO CHANGE "front" AND "back"
    robot_vector = (front[0] - back[0], front[1] - back[1])

    # Calculate the vector from the front of the robot to the target position
    target_vector = (int(ball[0]) - int(back[0]), int(ball[1]) - int(back[1]))

    # Calculate the signed angle between the robot vector and the target vector
    angle_radians = math.atan2(target_vector[1], target_vector[0]) - math.atan2(robot_vector[1], robot_vector[0])
    angle_degrees = math.degrees(angle_radians)

    if angle_degrees < -180:
        angle_degrees += 360
    if angle_degrees > 180:
        angle_degrees -= 360

    # Normalize the angle to be within the range of -180 to 180 degrees

    # print(180 - angle_degrees)

    return angle_degrees


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


# MIGHT NOT WORK PROPERLY
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
# Change has been added to this function so it is now a collect balls method
def collect_balls(image):
    print("Now doing image recognition")
    front, back, balls = detectRobotAndBalls.imageRecognitionHD(image)
    # Temporary if statement
    if front is None or back is None:
        return Moves.MoveClass(MoveTypes.TURN, 500, 50)
    nearest_ball, distance = find_nearest_ball(front, balls)

    print("The turn will now be calculated with: ")
    print(str(front))
    print(str(back))
    print(str(nearest_ball))

    angle_to_turn = calculate_turn(back, front, nearest_ball)
    print(angle_to_turn)

    if angle_to_turn > 5 or angle_to_turn < -5:
        print("I should turn: " + str(angle_to_turn))
        print(str(angle_to_turn) + " degrees")
        return Moves.MoveClass(MoveTypes.TURN, 500, angle_to_turn)
    else:
        return Moves.MoveClass(MoveTypes.FORWARD, 500, 1000)


def move_to_goal(image, point):
    front_pos, back_pos, ball_locations = detectRobotAndBalls.imageRecognitionHD(image)
    angle_to_turn = calculate_turn(back_pos, front_pos, point)

    if front_pos is None or back_pos is None:
        return Moves.MoveClass(MoveTypes.TURN, 500, 50)

    if robot_center_coordinates(front_pos, back_pos)[1] > point[1] + 10 & robot_center_coordinates(front_pos, back_pos)[
        1] < point[1] - 10:
        return "done"
    if angle_to_turn > 5 or angle_to_turn < -5:
        print("I should turn: " + str(angle_to_turn))
        print(str(angle_to_turn) + " degrees")
        return Moves.MoveClass(MoveTypes.TURN, 500, angle_to_turn[1])
    if front_pos[0] > point[0]:
        return Moves.MoveClass(MoveTypes.BACKWARD, 500, 10)
    else:
        return Moves.MoveClass(MoveTypes.FORWARD, 500, 1000)


def deliver_balls(image, field):
    front_pos, back_pos, ball_locations = detectRobotAndBalls.imageRecognitionHD(image)
    print("Front_pos: " + str(front_pos))
    print("Back_pos: " + str(back_pos))

    # As of right now I assume the first big goal i get is the correct one
    print(len(field.small_goal))

    if len(field.large_goal) == 0:
        print("big goal is none")
        field.large_goal.append([1142, 375])
    if len(field.small_goal) == 0:
        field.small_goal.append([300, 375])

    print("big_goal: " + str(field.large_goal[0]))
    # I make the same assumption with the small goal
    print("small_goal`: " + str(field.small_goal[0]))
    robot_center = robot_center_coordinates(front_pos, back_pos)
    horizontal_to_goal = [robot_center[0], field.small_goal[1]]
    small_goal = field.small_goal
    angle = calculate_turn(back_pos, front_pos, field.large_goal)

    if angle < 5 & int(angle) > -5:
        if robot_center[1] > small_goal[1] + 10 & \
                robot_center[1] < small_goal[1] - 10:
            if robot_center[0] > small_goal[0] + 90 & \
                    robot_center[0] < small_goal[0] + 110:
                if front_pos[0] > back_pos[0]:
                    return Moves.MoveClass(MoveTypes.DELIVER, 0, 0)
                else:
                    return Moves.MoveClass(MoveTypes.TURN, 350, 180)
            else:
                return move_to_goal(image, small_goal)

    return move_to_goal(image, horizontal_to_goal)
