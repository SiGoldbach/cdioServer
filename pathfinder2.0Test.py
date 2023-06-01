import math

# import main


goal_x = 0
goal_y = 0


def find_nearest_ball(robot_x, robot_y, ball_locations):
    closest_distance = float('inf')
    closest_coordinate = []

    for coordinate in ball_locations:
        x = coordinate[0]
        y = coordinate[1]
        distance = math.sqrt((x - robot_x) ** 2 + (y - robot_y) ** 2)

        if distance < closest_distance:
            closest_distance = distance
            closest_coordinate = coordinate

    return closest_coordinate, closest_distance


def calculate_angle(ball_x, ball_y, robot_x, robot_y):
    angle = math.atan2(ball_y - robot_y, ball_x - robot_x) * (180 / math.pi)
    return angle


def make_move():
    ball_locations = [[2, 4], [2, 3], [8, 8], [8, 3], [10, 10], [20, 20], [1, 9], [16, 14]]  # Example of table balls
    orange_ball = [0, 0]  # the orange ball
    robot_location = [0, 0]  # example of robot location
    obstacles = [[5, 5], [5, 6], [5, 7], [5, 8], [5, 9]]  # Example obstacle coordinates (representing a wall)
    grid_size = [21, 21]  # Grid size representing the workspace
    closest_ball_location, distanceToBall = find_nearest_ball(robot_location[0], robot_location[1], ball_locations)
    angle_to_turn = calculate_angle(closest_ball_location[0], closest_ball_location[1], robot_location[0],
                                    robot_location[1])
    return distanceToBall, angle_to_turn


distance, angle = make_move()
print("Distance is: "+str(distance))
print("Angle is: "+str(angle))
