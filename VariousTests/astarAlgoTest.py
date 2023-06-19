import heapq
import matplotlib.pyplot as plt


# Define the heuristic function (Manhattan distance)
def heuristic(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


# Define the A* algorithm function
def astar(start, goal, obstacles, obstacle_threshold):
    open_set = []
    closed_set = set()
    came_from = {}

    # Initialize the start node
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    heapq.heappush(open_set, (f_score[start], start))

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
            return path

        closed_set.add(current)

        # Generate the neighboring nodes
        neighbors = []
        x, y = current
        possible_moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1),
                          (x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)]
        for neighbor in possible_moves:
            valid_neighbor = True

            # Check if the neighbor is within bounds
            if not (0 <= neighbor[0] < GRID_WIDTH and 0 <= neighbor[1] < GRID_HEIGHT):
                valid_neighbor = False

            # Check if the neighbor is too close to any obstacle
            for obstacle in obstacles:
                if abs(neighbor[0] - obstacle[0]) <= obstacle_threshold and abs(
                        neighbor[1] - obstacle[1]) <= obstacle_threshold:
                    valid_neighbor = False
                    break

            if valid_neighbor:
                neighbors.append(neighbor)

        for neighbor in neighbors:
            # Calculate the tentative g_score
            tentative_g_score = g_score[current] + 1

            if neighbor in closed_set and tentative_g_score >= g_score.get(neighbor, float('inf')):
                continue

            if tentative_g_score < g_score.get(neighbor, float('inf')) or neighbor not in [i[1] for i in open_set]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    # If no path is found
    return None


# Define the dimensions of the grid
GRID_WIDTH = 100
GRID_HEIGHT = 100

# Define the start and goal coordinates
start = (1, 1)
goal = (90, 90)

# Define the coordinates of the obstacles
obstacles = [
    (30, 40),
    (40, 30),
    (50, 60),
    (60, 50),
    (70, 20),
    (20, 70),
    (20, 55),
    (55, 20),
    (39, 39)
]

# Define the distance threshold to avoid obstacles
obstacle_threshold = 5

# Find the path using A* algorithm
path = astar(start, goal, obstacles, obstacle_threshold)

# Visualize the grid, obstacles, and path
plt.figure(figsize=(8, 8))
plt.xlim(0, GRID_WIDTH)
plt.ylim(0, GRID_HEIGHT)
plt.title('A* Algorithm - Path Planning')
plt.xlabel('X')
plt.ylabel('Y')

# Plot the obstacles
for obstacle in obstacles:
    plt.scatter(obstacle[0], obstacle[1], color='red', marker='s', s=80)

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
