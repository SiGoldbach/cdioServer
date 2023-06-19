import heapq
import matplotlib.pyplot as plt


# Define the heuristic function (Manhattan distance)
def heuristic(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


# Define a QuadTree data structure to efficiently store and query obstacles
class QuadTree:
    def __init__(self, boundary, capacity=4):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False

    def insert(self, point):
        if not self.boundary.contains_point(point):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True

        if not self.divided:
            self.subdivide()

        if self.northwest.insert(point):
            return True
        if self.northeast.insert(point):
            return True
        if self.southwest.insert(point):
            return True
        if self.southeast.insert(point):
            return True

        return False

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w / 2
        h = self.boundary.h / 2

        nw_boundary = Boundary(x - w, y - h, w, h)
        ne_boundary = Boundary(x + w, y - h, w, h)
        sw_boundary = Boundary(x - w, y + h, w, h)
        se_boundary = Boundary(x + w, y + h, w, h)

        self.northwest = QuadTree(nw_boundary, self.capacity)
        self.northeast = QuadTree(ne_boundary, self.capacity)
        self.southwest = QuadTree(sw_boundary, self.capacity)
        self.southeast = QuadTree(se_boundary, self.capacity)

        self.divided = True

    def query_range(self, boundary):
        points = []
        if not self.boundary.intersects(boundary):
            return points

        for point in self.points:
            if boundary.contains_point(point):
                points.append(point)

        if self.divided:
            points += self.northwest.query_range(boundary)
            points += self.northeast.query_range(boundary)
            points += self.southwest.query_range(boundary)
            points += self.southeast.query_range(boundary)

        return points


# Define a Boundary class to represent a rectangular boundary
class Boundary:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains_point(self, point):
        return (self.x - self.w) <= point[0] <= (self.x + self.w) and (self.y - self.h) <= point[1] <= (self.y + self.h)

    def intersects(self, other):
        return not (self.x - self.w > other.x + other.w or self.x + self.w < other.x - other.w or
                    self.y - self.h > other.y + other.h or self.y + self.h < other.y - other.h)


# Define the A* algorithm function
def astar(start, goal, obstacles, obstacle_threshold):
    open_set = []
    closed_set = set()
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    heapq.heappush(open_set, (f_score[start], start))

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        closed_set.add(current)

        neighbors = []
        x, y = current
        possible_moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1),
                          (x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)]
        for neighbor in possible_moves:
            valid_neighbor = True
            if not (0 <= neighbor[0] < GRID_WIDTH and 0 <= neighbor[1] < GRID_HEIGHT):
                valid_neighbor = False

            neighbor_boundary = Boundary(neighbor[0], neighbor[1], obstacle_threshold, obstacle_threshold)
            nearby_obstacles = obstacle_quadtree.query_range(neighbor_boundary)
            if nearby_obstacles:
                valid_neighbor = False

            if valid_neighbor:
                neighbors.append(neighbor)

        for neighbor in neighbors:
            tentative_g_score = g_score[current] + 1

            if neighbor in closed_set and tentative_g_score >= g_score.get(neighbor, float('inf')):
                continue

            if tentative_g_score < g_score.get(neighbor, float('inf')) or neighbor not in [i[1] for i in open_set]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None


# Define the dimensions of the grid
GRID_WIDTH = 100
GRID_HEIGHT = 100

# Define the start and goal coordinates
start = (1, 1)
goal = (90, 90)

# Define the coordinates of the obstacles
obstacles = [
    (10, 88),
    (30, 40),
    (40, 30),
    (20, 70),
    (20, 55),
    (55, 20),
    (39, 39)
]

# Define the distance threshold to avoid obstacles
obstacle_threshold = 4

# Create the QuadTree and insert obstacles
obstacle_boundary = Boundary(0, 0, GRID_WIDTH, GRID_HEIGHT)
obstacle_quadtree = QuadTree(obstacle_boundary)
for obstacle in obstacles:
    obstacle_quadtree.insert(obstacle)

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