import math
import Moves
import MoveTypes
import Pathfinder


def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def move_forward(distance):
    Moves.MoveClass(MoveTypes.FORWARD, 500, distance)


def turn(angle):
    Moves.MoveClass(MoveTypes.TURN, 500, angle)


def astar(front_pos, back_pos, goal, obstacle):
    robot_center = Pathfinder.robot_center_coordinates(front_pos=front_pos, back_pos=back_pos)
    path = []

    # Calculate the angle and distance to navigate around the obstacle
    obstacle_distance = distance(front_pos, obstacle[0])
    obstacle_angle = Pathfinder.calculate_turn(back_pos=back_pos, front_pos=front_pos, ball_pos=obstacle[0])

    # Move to the side of the obstacle
    turn(obstacle_angle)
    move_forward(obstacle_distance)

    # Calculate the angle and distance to reach the goal from the side of the obstacle
    goal_distance = distance(obstacle[0], goal)
    goal_angle = Pathfinder.calculate_turn(front_pos=obstacle[0], back_pos=back_pos, ball_pos=goal)

    # Turn towards the goal without going through the obstacle
    turn(goal_angle)

    # Calculate the distance to move parallel to the obstacle
    parallel_distance = distance(obstacle[0], obstacle[1])

    # Move parallel to the obstacle
    move_forward(parallel_distance)

    # Calculate the angle and distance to reach the goal from the parallel position
    goal_distance_parallel = distance(obstacle[1], goal)
    goal_angle_parallel = Pathfinder.calculate_turn(front_pos=obstacle[1], back_pos=back_pos, ball_pos=goal)

    # Turn towards the goal from the parallel position
    turn(goal_angle_parallel)

    # Move forward towards the goal
    move_forward(goal_distance_parallel)

    # Append the visited positions to the path
    path.append(front_pos)
    path.append(obstacle[0])
    path.append(obstacle[1])
    path.append(goal)

    return path


# Example usage
front_pos = (0, 0)
back_pos = (1, 0)
goal = (12, 14)
obstacle = [(5, 5), (-6, 14), (10, 10), (12, 8)]  # Square obstacle represented by its four corners

path = astar(front_pos, back_pos, goal, obstacle)
print("Path:", path)
