import math
import heapq
import MoverFinder

# import main

coordinates_array = [[2, 4], [6, 3], [8, 8], [8, 3], [10, 10], [20, 20], [1, 9], [16, 14]] # Example of table tennis balls
robot_location = [[0, 0]] # example of robot location
obstacles = [[5, 5], [5, 6], [5, 7], [5, 8], [5, 9]]  # Example obstacle coordinates (representing a wall)
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

def astar_pathfinding(start_x, start_y, target_x, target_y, grid, obstacles):
    start_node = Node(start_x, start_y)
    target_node = Node(target_x, target_y)

    open_set = []
    closed_set = set()

    heapq.heappush(open_set, start_node)

    while open_set:
        current_node = heapq.heappop(open_set)

        if current_node.x == target_node.x and current_node.y == target_node.y:
            path = []
            while current_node:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            return list(reversed(path))

        closed_set.add((current_node.x, current_node.y))

        neighbors = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor_x = current_node.x + dx
            neighbor_y = current_node.y + dy

            if (
                0 <= neighbor_x < len(grid) and
                0 <= neighbor_y < len(grid[0]) and
                grid[neighbor_x][neighbor_y] != 1
            ):
                neighbors.append(Node(neighbor_x, neighbor_y))

        for neighbor in neighbors:
            if (neighbor.x, neighbor.y) in closed_set:
                continue

            neighbor_g = current_node.g + 1

            in_open_set = False
            for node in open_set:
                if node.x == neighbor.x and node.y == neighbor.y:
                    in_open_set = True
                    break

            if not in_open_set or neighbor_g < neighbor.g:
                neighbor.g = neighbor_g
                neighbor.h = math.sqrt((neighbor.x - target_x) ** 2 + (neighbor.y - target_y) ** 2)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current_node

                if not in_open_set:
                    heapq.heappush(open_set, neighbor)

    return None

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


def move_robot(target_x, target_y):
    global robot_x, robot_y
    path = astar_pathfinding(robot_x, robot_y, target_x, target_y, grid, obstacles)
    print("Moving robot from", (robot_x, robot_y), "to", (target_x, target_y))


    if path:
        for i in range(1, len(path)):
            next_x, next_y = path[i]
            robot_x = next_x
            robot_y = next_y
            print("Moving to:", (robot_x, robot_y))
    else:
        print("No valid path found!")

    # Calculate the angle and distance to the next move
    angle = calculate_angle(target_x, target_y, robot_x, robot_y)
    distance = math.sqrt((target_x - robot_x) ** 2 + (target_y - robot_y) ** 2)

    capacity_full = False
    if counter % 6 == 0 | len(coordinates_array) == 0:
        capacity_full = True

    return angle, distance

# Create the grid based on the workspace size
grid = [[0 for _ in range(grid_size[1])] for _ in range(grid_size[0])]

# Mark the obstacle cells in the grid
for obstacle in obstacles:
    obstacle_x, obstacle_y = obstacle
    grid[obstacle_x][obstacle_y] = 1

# Initialize counter
counter = 0

# Main loop to process each target
while coordinates_array:
    # Find the closest coordinates and distance
    closest_coordinates, closest_distance = find_nearest_ball(robot_x, robot_y, coordinates_array)
    print("Closest coordinates:", closest_coordinates)

    # Calculate the angle between the robot's current location and the target
    angle = calculate_angle(closest_coordinates[0], closest_coordinates[1], robot_x, robot_y)

    # Move the robot to the target
    move_robot(closest_coordinates[0], closest_coordinates[1])

    # Increment the counter
    counter += 1
    print("Current targets reached:", counter)
    print(angle)
    print(closest_distance)
    print(closest_coordinates)

    # Remove the target coordinates from the array
    coordinates_array.remove(closest_coordinates)

    if counter % 6 == 0 | len(coordinates_array) == 0:
        angle, distance = move_robot(goal_x, goal_y)
        # turn back towards the goal
        # main.turn(200, 180)
        # open the hatch to release balls
        # main.openCloseHatch()
        # turn around again
        # main.turn(200, 180)
        print("we unloaded")


# After processing all targets
print("All targets processed.")
print("Total targets reached:", counter)
print(angle)

def next_move(frame):
    closest_coordinates, closest_distance = find_nearest_ball(robot_x, robot_y, coordinates_array)
    angle = calculate_angle(closest_coordinates[0], closest_coordinates[1], robot_x, robot_y)
    move_robot(closest_coordinates[0], closest_coordinates[1])

    return closest_distance, closest_coordinates, angle
    print("Finding the next move")


