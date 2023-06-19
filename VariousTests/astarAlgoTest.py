import heapq
import math
import numpy as np
import matplotlib.pyplot as plt

grid_size = (10, 10)  # Adjust the size according to your requirements
start = (4, 0)  # Starting position
goal = (4, 8)  # Goal position
obstacle = (4, 4)  # Obstacle position


def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def astar(start, goal, obstacle):
    # Define possible movements (up, down, left, right, diagonal)
    movements = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]

    # Initialize data structures
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while open_list:
        current_cost, current = heapq.heappop(open_list)

        if current == goal:
            break

        for movement in movements:
            dx, dy = movement
            next_pos = (current[0] + dx, current[1] + dy)

            if (
                    next_pos[0] < 0
                    or next_pos[0] >= grid_size[0]
                    or next_pos[1] < 0
                    or next_pos[1] >= grid_size[1]
            ):
                continue

            new_cost = cost_so_far[current] + euclidean_distance(current, next_pos)

            if next_pos == obstacle:
                new_cost += float('inf')  # Make the cost infinitely high for the obstacle

            if (
                    next_pos not in cost_so_far
                    or new_cost < cost_so_far[next_pos]
            ):
                cost_so_far[next_pos] = new_cost
                priority = new_cost + euclidean_distance(goal, next_pos)
                heapq.heappush(open_list, (priority, next_pos))
                came_from[next_pos] = current

    # Retrieve the path
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    return path


path = astar(start, goal, obstacle)

# Plotting the grid
grid = np.zeros(grid_size)
grid[obstacle] = 1
plt.imshow(grid, cmap='binary')

# Plotting the obstacle
plt.scatter(obstacle[1], obstacle[0], color='red', marker='s')

# Plotting the path
path_x, path_y = zip(*path)
plt.plot(path_y, path_x, marker='o')

# Plotting the start and goal positions
plt.scatter(start[1], start[0], color='green', marker='o')
plt.scatter(goal[1], goal[0], color='blue', marker='o')

# Display the plot
plt.show()
