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
    robot_vector = (int(front[0]) - int(back[0]), int(front[1]) - int(back[1]))

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

    return MoveTypes.TURN, angle_degrees


def calculate_turn_2(front_pos, back_pos, target_pos):
    robot_middle = (front_pos[0] + back_pos[0]) / 2, (front_pos[1] + back_pos[1]) / 2
    robot_vector = (int(robot_middle[0]) - int(front_pos[0]), int(back_pos[1]) - int(front_pos[1]))
    # Calculate the vector from the front of the robot to the target position
    target_vector = (int(target_pos[0]) - int(front_pos[0]), int(target_pos[1]) - int(front_pos[1]))
    # Calculate the signed angle between the robot vector and the target vector
    angle_radians = math.atan2(target_vector[1], target_vector[0]) - math.atan2(robot_vector[1], robot_vector[0])
    angle_degrees = math.degrees(angle_radians)
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


def calculate_possible_max_turn(front_pos, back_pos, obstacles):
    # Calculate the max turn angle the robot can make before hitting an obstacle

    # Determine the robot's orientation
    robot_orientation = math.atan2(back_pos[1] - front_pos[1], back_pos[0] - front_pos[0])

    # Calculate the vectors to the obstacles
    obstacle_vectors = [(obstacle[0] - front_pos[0], obstacle[1] - front_pos[1]) for obstacle in obstacles]

    # Calculate the angles between the robot's orientation and the obstacle vectors
    relative_angles = [math.degrees(math.atan2(vector[1], vector[0]) - robot_orientation) for vector in
                       obstacle_vectors]

    # Determine the available turning space
    min_angle = min(relative_angles)
    max_angle = max(relative_angles)
    available_turn_space = max_angle - min_angle

    return available_turn_space


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


def find_obstacle_in_circle(obstacles, front_pos, back_pos):
    robot_length = get_robot_length(front_pos, back_pos)
    robot_center = robot_center_coordinates(front_pos, back_pos)
    robot_radius = robot_length / 2
    obstacles_in_range = []
    print(robot_center)
    print(robot_radius)
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

    if angle_to_turn[1] > 5 or angle_to_turn[1] < -5:
        print("I should turn: " + str(angle_to_turn))
        print(str(angle_to_turn) + " degrees")
        return Moves.MoveClass(MoveTypes.TURN, 500, angle_to_turn[1])
    else:
        return Moves.MoveClass(MoveTypes.FORWARD, 500, 1000)


def drive_to_goal(image):
    front_pos, back_pos, ball_locations = detectRobotAndBalls.imageRecognitionHD(image)
    smallGoal, bigGoal, obstacle, corners = detectField.imageRecognitionHD(image)
    print("Front_pos: " + str(front_pos))
    print("Back_pos: " + str(back_pos))
    # As of right now I assume the first big goal i get is the correct one
    print(len(bigGoal))
    if len(bigGoal) == 0:
        print("big goal is none")
        bigGoal.append([1142, 375])
    if len(smallGoal) == 0:
        smallGoal.append([300, 375])
    print("big_goal: " + str(bigGoal[0]))
    # I make the same assumption with the small goal
    print("small_goal`: " + str(smallGoal[0]))

    angleToTurn = calculate_turn(front_pos, back_pos, bigGoal[0])
    print("Angle tu turn is from back: " + str(angleToTurn))
    # Here angle to turn is calculated from the front since the angle here needs to be low for the two
    # vectors to point the same direction
    # I here need to have three cases one i the robot is ready to deliver
    # 1: can the robot deliver the balls as it is standing right now
    # 2: Is the robot close enough to the line where it just needs to drive backwards to reach the goal
    # 3: Is the robot some random place on the field
    # If the robot enters this if statement it is oriented correctly and should just back or deliver
    # This is taking care of condition 1
    if -7 < angleToTurn[1] < 7:
        print("Robot is close to aligned to the center")
        # I will now figure out what direction the robot has and how close to the goal the robot is
        front_to_goal = math.sqrt((bigGoal[0][0] - front_pos[0]) ** 2 + (bigGoal[0][1] - front_pos[1]) ** 2)
        print("Length from front to goal is: " + str(front_to_goal))
        back_to_goal = math.sqrt((bigGoal[0][0] - back_pos[0]) ** 2 + (bigGoal[0][1] - back_pos[1]) ** 2)
        print("Length from back to goal is: " + str(back_to_goal))
        if back_to_goal < 340:
            # When the robots back
            print("I will deliver")
            return Moves.MoveClass(MoveTypes.DELIVER, 0, 0)
        else:
            print("I will go back")
            # The length of the backwards move is a bit arbitrary right now
            # should probably be a pretty low value
            Moves.MoveClass(MoveTypes.BACKWARD, 500, 30)
    # This is taking further care of condition 2
    if -175 > angleToTurn[1] or 175 < angleToTurn[1]:
        # Here the robot should turn 180 degrees
        return Moves.MoveClass(MoveTypes.TURN, 500, 180)

    # A problem here is that the robot should not drive to the goal but rather a point somewhat in front of the goal
    # Therefore I will calculate the center of the field base on

    # Now for number three here the robot should first turn into the point and then afterwards

    center_of_field = [
        ((int(bigGoal[0][0])) + (int(smallGoal[0][0]))) / 2, ((int(bigGoal[0][1])) + (int(smallGoal[0][1]))) / 2]
    print("center_of_field: " + str(center_of_field))
    goal_coordinate = [(int(bigGoal[0][0]) + center_of_field[0]) / 2, center_of_field[1]]
    print("I will try to go to this coordinate: " + str(goal_coordinate))

    # Here I am calculating the turn needed to go to the arbitrary point
    angle_to_goal = calculate_turn(back_pos, front_pos, goal_coordinate)
    print("I should turn: " + str(angle_to_goal) + " so i can drive to the preset point")

    if 6 < angle_to_goal[1] < -6:
        print("I am already turned the correct directio")
        print(str(angle_to_goal[1]) + " degrees")
        # need to find distance moved for argument
        return Moves.MoveClass(angle_to_goal[0], 500, 400)
    else:
        return Moves.MoveClass(angle_to_goal[0], 500, angle_to_goal[1])
