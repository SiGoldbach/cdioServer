import math

import MoverFinder
import moveOptions

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

def find_goal_distance(goal_x, goal_y, robot_x, robot_y):
    goal_distance = math.sqrt((goal_x - robot_x) ** 2 + (goal_y - robot_y) ** 2)
    return goal_distance


def make_move(frame):
    ball_locations = [[2, 4], [2, 3], [8, 8], [8, 3], [10, 10], [20, 20], [1, 9], [16, 14]]  # Example of table balls
    orange_ball = [0, 0]  # the orange ball
    robot_location = [0, 0]  # example of robot location
    obstacles = [[5, 5], [5, 6], [5, 7], [5, 8], [5, 9]]  # Example obstacle coordinates (representing a wall)
    grid_size = [21, 21]  # Grid size representing the workspace
    closest_ball_location, distanceToBall = find_nearest_ball(robot_location[0], robot_location[1], ball_locations)
    angle_to_turn = calculate_angle(closest_ball_location[0], closest_ball_location[1], robot_location[0],
                                    robot_location[1])
    angle_to_goal = calculate_angle(goal_x, goal_y, robot_location[0], robot_location[1])
    goalDistance = find_goal_distance(goal_x, goal_y, robot_location[0], robot_location[1])

    if angle_to_goal > 0 & len(ball_locations) == 5 | 3 | 2 | 1:
        return MoverFinder.MoveClass(moveOptions.RIGHT, 300, angle_to_goal), MoverFinder.MoveClass(moveOptions.FORWARD,
                                                                                                   500, goalDistance)
    if angle_to_goal < 0 & len(ball_locations) == 5 | 3 | 2 | 1:
        return MoverFinder.MoveClass(moveOptions.LEFT, 300, angle_to_goal), MoverFinder.MoveClass(moveOptions.FORWARD,
                                                                                                  500, goalDistance)
    if angle_to_goal == 0 & len(ball_locations) == 5 | 3 | 2 | 1:
        return MoverFinder.MoveClass(moveOptions.FORWARD, 500, goalDistance)

    if angle_to_turn > 0:
        return MoverFinder.MoveClass(moveOptions.RIGHT, 300, angle_to_turn), MoverFinder.MoveClass(moveOptions.FORWARD,
                                                                                                   500, distanceToBall)
    if angle_to_turn == 0:
        return MoverFinder.MoveClass(moveOptions.FORWARD, 500, distanceToBall)

    if angle_to_turn < 0:
        return MoverFinder.MoveClass(moveOptions.LEFT, 300, angle_to_turn), MoverFinder.MoveClass(moveOptions.FORWARD,
                                                                                                  500, distanceToBall)

    return MoverFinder.MoveClass(moveOptions.UNSTUCK, 500, 100)


angle, distance = make_move(None)
print("Distance is: ")
distance.print()
print("Angle is: ")
angle.print()
