import math


coordinates_array = [[2, 4], [6, 3], [8, 8], [8, 3], [10, 10], [20, 20], [1, 9],
                     [16, 14]]  # Example of table tennis balls
robot_location = [[0, 0]]  # example of robot location
obstacles = [[5, 5], [5, 6], [5, 14], [5, 8], [5, 9]]  # Example obstacle coordinates (representing a wall)
grid_size = [21, 21]  # Grid size representing the workspace
robot_x = 0
robot_y = 0
goal_x = 0
goal_y = 0


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f


def find_nearest_ball(robot_x, robot_y, coordinates_array):
    closest_distance = float('inf')
    closest_coordinate = []

    for coordinate in coordinates_array:
        x = coordinate[0]
        y = coordinate[1]
        distance = math.sqrt((x - robot_x) ** 2 + (y - robot_y) ** 2)

        if distance < closest_distance:
            closest_distance = distance
            closest_coordinate = coordinate

    return closest_coordinate, closest_distance


def calculate_angle(target_x, target_y, robot_x, robot_y):
    angle = math.atan2(target_y - robot_location[1], target_x - robot_location[0]) * (180 / math.pi)
    return angle


def calculate_line(target_x, target_y, robot_x, robot_y, x):
    m = ((target_y - robot_y) / (target_x - robot_x))
    b = robot_y - m * robot_x
    # vi skal parallelforskyde linjen med 16pixel hver vej. ergo b+16 | b-16
    line1 = [int(m), int(b + 16)]
    line2 = [int(m), int(b - 16)]

    return line1, line2


def check_for_obstacle(red_pixel, line1, line2):
    x, y = red_pixel
    # Calculate the y-values for each line at the given x-coordinate
    y1 = line1[0] * x + line1[1]
    y2 = line2[0] * x + line2[1]
    # Check if the point's y-coordinate is between the y-values of the lines
    if min(y1, y2) <= y <= max(y1, y2):
        return True
    else:
        return False
