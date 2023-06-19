import numpy as np
import heapq
import matplotlib.pyplot as plt

# Define the heuristic function (Manhattan distance)
def heuristic(node, goal):
    return np.abs(node[0] - goal[0]) + np.abs(node[1] - goal[1])

# Define the A* algorithm function
def astar(start, goal, obstacles, obstacle_threshold):
    GRID_WIDTH = 100
    GRID_HEIGHT = 100

    open_set = []
    closed_set = set()
    came_from = {}

    # Initialize the start node
    g_score = {}
    f_score = {}
    g_score[tuple(start)] = 0
    f_score[tuple(start)] = heuristic(start, goal)
    heapq.heappush(open_set, (f_score[tuple(start)], tuple(start)))

    # A* algorithm loop
    while open_set:
        current = heapq.heappop(open_set)[1]

        # Check if the goal is reached
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path[::5]  # Return every 5th coordinate in the path

        closed_set.add(tuple(current))  # Convert to tuple

        # Generate the neighboring nodes
        x, y = current
        moves = np.array([(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)])
        neighbors = np.add(current, moves)

        valid_neighbors = np.logical_and.reduce((
            neighbors[:, 0] >= 0,
            neighbors[:, 0] < GRID_WIDTH,
            neighbors[:, 1] >= 0,
            neighbors[:, 1] < GRID_HEIGHT,
        ))

        for neighbor in neighbors[valid_neighbors]:
            valid_neighbor = True

            # Check if the neighbor is too close to any obstacle
            for obstacle in obstacles:
                if np.abs(neighbor[0] - obstacle[0]) <= obstacle_threshold and np.abs(neighbor[1] - obstacle[1]) <= obstacle_threshold:
                    valid_neighbor = False
                    break

            if valid_neighbor:
                if tuple(neighbor) in closed_set and g_score[tuple(current)] + 1 >= g_score.get(tuple(neighbor), np.inf):
                    continue

                if g_score[tuple(current)] + 1 < g_score.get(tuple(neighbor), np.inf) or not any(
                        (neighbor == i[1]).all() for i in open_set):
                    came_from[tuple(neighbor)] = current  # Convert to tuple
                    g_score[tuple(neighbor)] = g_score[tuple(current)] + 1
                    f_score[tuple(neighbor)] = g_score[tuple(neighbor)] + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[tuple(neighbor)], tuple(neighbor)))

    # If no path is found
    return None


# Define the start and goal coordinates
start = (1, 1)
goal = (90, 90)

# Define the coordinates of the obstacles
obstacles = np.array([
    (30, 30),
    (70, 70),
    (20, 20),
    (80, 80),
    (20, 70),
    (20, 55),
    (55, 20),
    (39, 39)
])

# Define the distance threshold to avoid obstacles
obstacle_threshold = 5

# Find the path using A* algorithm
path = astar(start, goal, obstacles, obstacle_threshold)

# Visualize the grid, obstacles, and path
plt.figure(figsize=(8, 8))
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.title('A* Algorithm - Path Planning')
plt.xlabel('X')
plt.ylabel('Y')

# Plot the obstacles
plt.scatter(obstacles[:, 0], obstacles[:, 1], color='red', marker='s', s=80)

# Plot the path if it exists
if path is not None:
    x_path, y_path = zip(*path)
    plt.plot(x_path, y_path, color='blue', linewidth=2, label='Path')
else:
    print("No path found.")

# Plot the start and goal positions
plt.scatter(start[0], start[1], color='green', marker='o', s=80, label='Start')
plt.scatter(goal[0], goal[1], color='orange', marker='o', s=80, label='Goal')

plt.legend()
plt.grid(True)
plt.show()
