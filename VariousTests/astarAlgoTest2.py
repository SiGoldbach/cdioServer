import heapq
import numpy as np

GRID_WIDTH = 1280
GRID_HEIGHT = 720


# Define the heuristic function (Manhattan distance)
def heuristic(node, goal):
    return np.abs(node[0] - goal[0]) + np.abs(node[1] - goal[1])


# Define the A* algorithm function
def astar(start, goal, obstacles, obstacle_threshold):
    open_set = []
    closed_set = set()
    came_from = {}

    # Initialize the start node
    heapq.heappush(open_set, (heuristic(start, goal), start))

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

        closed_set.add(tuple(current))  # Convert tuple to tuple

        # Generate the neighboring nodes
        x, y = current
        possible_moves = np.array([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1),
                                  (x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)])
        valid_moves = np.logical_and.reduce((0 <= possible_moves[:, 0], possible_moves[:, 0] < GRID_WIDTH,
                                             0 <= possible_moves[:, 1], possible_moves[:, 1] < GRID_HEIGHT))

        # Check if the neighbor is too close to any obstacle
        valid_neighbors = []
        for move in possible_moves[valid_moves]:
            valid_neighbor = True
            for obstacle in obstacles:
                if np.abs(move[0] - obstacle[0]) <= obstacle_threshold and np.abs(move[1] - obstacle[1]) <= obstacle_threshold:
                    valid_neighbor = False
                    break
            if valid_neighbor:
                valid_neighbors.append(move)

        for neighbor in valid_neighbors:
            # Calculate the tentative g_score
            tentative_g_score = came_from.get(current, (float('inf'),)) + (1,)  # Calculate as a tuple

            if neighbor in closed_set and tentative_g_score >= came_from.get(neighbor, (float('inf'),)):
                continue

            if tentative_g_score < came_from.get(neighbor, (float('inf'),)) or neighbor not in [i[1] for i in open_set]:
                came_from[neighbor] = current
                heapq.heappush(open_set, (tentative_g_score + heuristic(neighbor, goal), neighbor))

    # If no path is found
    return None