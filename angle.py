import math

def calculate_angle(robot_back, robot_front, ball):
    # Calculate the vector from the back of the robot to the ball
    robot_to_ball = (ball[0] - robot_back[0], ball[1] - robot_back[1])

    # Calculate the vector representing the direction of the robot
    robot_direction = (robot_front[0] - robot_back[0], robot_front[1] - robot_back[1])

    # Calculate the dot product of the two vectors
    dot_product = robot_to_ball[0] * robot_direction[0] + robot_to_ball[1] * robot_direction[1]

    # Calculate the magnitudes of the two vectors
    robot_to_ball_magnitude = math.sqrt(robot_to_ball[0] ** 2 + robot_to_ball[1] ** 2)
    robot_direction_magnitude = math.sqrt(robot_direction[0] ** 2 + robot_direction[1] ** 2)

    # Calculate the angle in radians using the arccosine function
    angle_radians = math.acos(dot_product / (robot_to_ball_magnitude * robot_direction_magnitude))

    # Convert the angle to degrees
    angle_degrees = math.degrees(angle_radians)

    return angle_degrees

# Example usage
robot_back = (2, 2)
robot_front = (3, 3)
ball = (2.5, 3)

angle = calculate_angle(robot_back, robot_front, ball)
print("Angle:", angle)
