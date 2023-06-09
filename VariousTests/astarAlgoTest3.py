import heapq
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree


# Define the heuristic function (Manhattan distance)
def heuristic(node, end):
    dx = abs(node[0] - end[0])
    dy = abs(node[1] - end[1])
    diagonal_moves = min(dx, dy)
    straight_moves = abs(dx - dy)
    return diagonal_moves * 1.4 + straight_moves


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
def astar(start, goal, obstacles, obstacle_threshold, max_turning_points):
    open_set = []
    closed_set = set()
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    turning_points = {start: 0}  # Track the number of turning points for each node

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
            return path, turning_points

        closed_set.add(current)

        neighbors = []
        x, y = current
        possible_moves = [
            (x - 1, y), (x + 1, y),  # horizontal moves
            (x, y - 1), (x, y + 1),  # vertical moves
            (x - 1, y - 1), (x + 1, y - 1),  # diagonal moves
            (x - 1, y + 1), (x + 1, y + 1)  # diagonal moves
        ]

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
                turning_points[neighbor] = turning_points[current] + 1  # Increase the turning point count
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None, None


# Define the dimensions of the grid
GRID_WIDTH = 1280
GRID_HEIGHT = 720

# Define the start and goal coordinates
start = (600, 0)
goal = (450, 450)


# Define the coordinates of the obstacles
obstacles = [[583, 309], [584, 308], [585, 308], [586, 308], [587, 308], [588, 308], [589, 308], [590, 308], [591, 308],
             [592, 309], [593, 309], [594, 309], [595, 310], [596, 311], [596, 312], [597, 313], [597, 314], [597, 315],
             [596, 316], [596, 317], [596, 318], [596, 319], [595, 320], [595, 321], [595, 322], [595, 323], [595, 324],
             [595, 325], [595, 326], [595, 327], [595, 328], [595, 329], [595, 330], [595, 331], [595, 332], [595, 333],
             [595, 334], [594, 335], [594, 336], [594, 337], [594, 338], [594, 339], [594, 340], [594, 341], [593, 342],
             [593, 343], [593, 344], [593, 345], [594, 345], [595, 345], [596, 345], [597, 346], [598, 346], [599, 346],
             [600, 347], [601, 347], [602, 347], [603, 347], [604, 347], [605, 347], [606, 347], [607, 347], [608, 347],
             [609, 347], [610, 348], [611, 348], [612, 348], [613, 348], [614, 348], [615, 348], [616, 348], [617, 348],
             [618, 348], [619, 348], [620, 348], [621, 349], [622, 349], [623, 349], [624, 349], [625, 349], [626, 350],
             [627, 350], [628, 351], [628, 352], [628, 353], [628, 354], [628, 355], [628, 356], [628, 357], [628, 358],
             [628, 359], [628, 360], [628, 361], [628, 362], [628, 363], [627, 364], [626, 364], [625, 364], [624, 364],
             [623, 364], [622, 364], [621, 364], [620, 364], [619, 364], [618, 363], [617, 363], [616, 363], [615, 363],
             [614, 363], [613, 363], [612, 363], [611, 363], [610, 363], [609, 363], [608, 363], [607, 363], [606, 363],
             [605, 363], [604, 363], [603, 362], [602, 362], [601, 362], [600, 362], [599, 362], [598, 362], [597, 362],
             [596, 362], [595, 362], [594, 362], [593, 362], [592, 362], [591, 362], [591, 363], [591, 364], [591, 365],
             [591, 366], [591, 367], [590, 368], [590, 369], [590, 370], [590, 371], [590, 372], [590, 373], [590, 374],
             [590, 375], [590, 376], [590, 377], [590, 378], [590, 379], [590, 380], [590, 381], [589, 382], [589, 383],
             [589, 384], [589, 385], [588, 386], [588, 387], [588, 388], [588, 389], [588, 390], [588, 391], [588, 392],
             [588, 393], [588, 394], [588, 395], [587, 396], [586, 396], [585, 397], [584, 397], [583, 397], [582, 397],
             [581, 397], [580, 397], [579, 397], [578, 397], [577, 397], [576, 396], [575, 396], [574, 395], [573, 394],
             [572, 393], [572, 392], [572, 391], [573, 390], [573, 389], [573, 388], [573, 387], [573, 386], [573, 385],
             [573, 384], [573, 383], [573, 382], [573, 381], [573, 380], [573, 379], [573, 378], [573, 377], [573, 376],
             [573, 375], [574, 374], [574, 373], [574, 372], [574, 371], [574, 370], [574, 369], [574, 368], [574, 367],
             [574, 366], [574, 365], [574, 364], [574, 363], [574, 362], [574, 361], [574, 360], [573, 360], [572, 360],
             [571, 360], [570, 359], [569, 359], [568, 359], [567, 359], [566, 359], [565, 359], [564, 359], [563, 358],
             [562, 358], [561, 358], [560, 358], [559, 358], [558, 358], [557, 358], [556, 358], [555, 358], [554, 358],
             [553, 357], [552, 357], [551, 357], [550, 357], [549, 357], [548, 357], [547, 357], [546, 357], [545, 357],
             [544, 357], [543, 356], [542, 356], [541, 355], [540, 354], [539, 353], [539, 352], [538, 351], [538, 350],
             [539, 349], [539, 348], [539, 347], [540, 346], [540, 345], [540, 344], [541, 343], [542, 342], [543, 341],
             [544, 341], [545, 341], [546, 340], [547, 340], [548, 340], [549, 341], [550, 341], [551, 341], [552, 341],
             [553, 341], [554, 341], [555, 341], [556, 341], [557, 341], [558, 341], [559, 341], [560, 342], [561, 342],
             [562, 342], [563, 342], [564, 342], [565, 342], [566, 342], [567, 342], [568, 342], [569, 342], [570, 342],
             [571, 343], [572, 343], [573, 343], [574, 343], [575, 343], [576, 343], [577, 342], [577, 341], [577, 340],
             [577, 339], [577, 338], [577, 337], [577, 336], [578, 335], [578, 334], [578, 333], [578, 332], [578, 331],
             [578, 330], [578, 329], [578, 328], [578, 327], [578, 326], [578, 325], [579, 324], [579, 323], [579, 322],
             [579, 321], [579, 320], [579, 319], [580, 318], [580, 317], [580, 316], [580, 315], [580, 314], [580, 313],
             [580, 312], [581, 311], [581, 310], [582, 309], [584, 308], [583, 309], [582, 309], [581, 309], [581, 310],
             [581, 311], [580, 312], [580, 313], [580, 314], [580, 315], [580, 316], [580, 317], [580, 318], [579, 319],
             [579, 320], [579, 321], [579, 322], [579, 323], [579, 324], [578, 325], [578, 326], [578, 327], [578, 328],
             [578, 329], [578, 330], [578, 331], [578, 332], [578, 333], [578, 334], [578, 335], [577, 336], [577, 337],
             [577, 338], [577, 339], [577, 340], [577, 341], [576, 342], [575, 343], [574, 343], [573, 343], [572, 343],
             [571, 343], [570, 342], [569, 342], [568, 342], [567, 342], [566, 342], [565, 342], [564, 342], [563, 342],
             [562, 342], [561, 342], [560, 342], [559, 341], [558, 341], [557, 341], [556, 341], [555, 341], [554, 341],
             [553, 341], [552, 341], [551, 341], [550, 341], [549, 341], [548, 340], [547, 340], [546, 340], [545, 341],
             [544, 341], [543, 341], [542, 341], [541, 342], [541, 343], [540, 344], [540, 345], [539, 346], [539, 347],
             [539, 348], [539, 349], [538, 350], [538, 351], [539, 352], [539, 353], [539, 354], [540, 355], [541, 356],
             [542, 356], [543, 356], [544, 357], [545, 357], [546, 357], [547, 357], [548, 357], [549, 357], [550, 357],
             [551, 357], [552, 357], [553, 357], [554, 358], [555, 358], [556, 358], [557, 358], [558, 358], [559, 358],
             [560, 358], [561, 358], [562, 358], [563, 358], [564, 359], [565, 359], [566, 359], [567, 359], [568, 359],
             [569, 359], [570, 359], [571, 360], [572, 360], [573, 360], [574, 361], [574, 362], [574, 363], [574, 364],
             [574, 365], [574, 366], [574, 367], [574, 368], [574, 369], [574, 370], [574, 371], [574, 372], [574, 373],
             [574, 374], [573, 375], [573, 376], [573, 377], [573, 378], [573, 379], [573, 380], [573, 381], [573, 382],
             [573, 383], [573, 384], [573, 385], [573, 386], [573, 387], [573, 388], [573, 389], [572, 390], [572, 391],
             [572, 392], [572, 393], [572, 394], [573, 395], [574, 396], [575, 396], [576, 396], [577, 397], [578, 397],
             [579, 397], [580, 397], [581, 397], [582, 397], [583, 397], [584, 397], [585, 397], [586, 396], [587, 396],
             [588, 396], [588, 395], [588, 394], [588, 393], [588, 392], [588, 391], [588, 390], [588, 389], [588, 388],
             [588, 387], [588, 386], [589, 385], [589, 384], [589, 383], [590, 382], [590, 381], [590, 380], [590, 379],
             [590, 378], [590, 377], [590, 376], [590, 375], [590, 374], [590, 373], [590, 372], [590, 371], [590, 370],
             [590, 369], [590, 368], [591, 367], [591, 366], [591, 365], [591, 364], [591, 363], [592, 362], [593, 362],
             [594, 362], [595, 362], [596, 362], [597, 362], [598, 362], [599, 362], [600, 362], [601, 362], [602, 362],
             [603, 362], [604, 363], [605, 363], [606, 363], [607, 363], [608, 363], [609, 363], [610, 363], [611, 363],
             [612, 363], [613, 363], [614, 363], [615, 363], [616, 363], [617, 363], [618, 364], [619, 364], [620, 364],
             [621, 364], [622, 364], [623, 364], [624, 364], [625, 364], [626, 364], [627, 364], [628, 364], [628, 363],
             [628, 362], [628, 361], [628, 360], [628, 359], [628, 358], [628, 357], [628, 356], [628, 355], [628, 354],
             [628, 353], [628, 352], [628, 351], [628, 350], [627, 350], [626, 350], [625, 349], [624, 349], [623, 349],
             [622, 349], [621, 349], [620, 348], [619, 348], [618, 348], [617, 348], [616, 348], [615, 348], [614, 348],
             [613, 348], [612, 348], [611, 348], [610, 348], [609, 347], [608, 347], [607, 347], [606, 347], [605, 347],
             [604, 347], [603, 347], [602, 347], [601, 347], [600, 346], [599, 346], [598, 346], [597, 346], [596, 345],
             [595, 345], [594, 345], [593, 344], [593, 343], [593, 342], [594, 341], [594, 340], [594, 339], [594, 338],
             [594, 337], [594, 336], [594, 335], [595, 334], [595, 333], [595, 332], [595, 331], [595, 330], [595, 329],
             [595, 328], [595, 327], [595, 326], [595, 325], [595, 324], [595, 323], [595, 322], [595, 321], [595, 320],
             [596, 319], [596, 318], [596, 317], [597, 316], [597, 315], [597, 314], [597, 313], [597, 312], [596, 311],
             [596, 310], [595, 309], [594, 309], [593, 309], [592, 309], [591, 308], [590, 308], [589, 308], [588, 308],
             [587, 308], [586, 308], [585, 308]]

# Define the distance threshold to avoid obstacles
obstacle_threshold = 40


# Define a function to create a buffer zone around the obstacles
def create_buffer_zone(obstacles, buffer_distance):
    buffered_obstacles = []
    for obstacle in obstacles:
        x, y = obstacle
        buffered_obstacles.append((x - buffer_distance, y - buffer_distance))
        buffered_obstacles.append((x - buffer_distance, y + buffer_distance))
        buffered_obstacles.append((x + buffer_distance, y - buffer_distance))
        buffered_obstacles.append((x + buffer_distance, y + buffer_distance))
    return buffered_obstacles


# Define the buffer distance around obstacles
buffer_distance = 10


def distance(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return (dx ** 2 + dy ** 2) ** 0.5


def is_overlapping(point1, point2, size):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x2 - x1) < size and abs(y2 - y1) < size


# Update the turning_point_threshold and turning_point_limit values
turning_point_threshold = 100
turning_point_limit = 4


def optimize_path(path, turning_point_threshold, max_turning_points):
    if len(path) <= 2 or max_turning_points <= 0:
        return path

    optimized_path = [path[0]]
    turning_points = []
    for i in range(1, len(path) - 1):
        dx1 = path[i][0] - optimized_path[-1][0]
        dy1 = path[i][1] - optimized_path[-1][1]
        dx2 = path[i + 1][0] - path[i][0]
        dy2 = path[i + 1][1] - path[i][1]
        if dx1 != dx2 or dy1 != dy2:
            if are_points_close(path[i], turning_points, turning_point_threshold):
                optimized_path.append(path[i])
                turning_points.append(path[i])
                if len(turning_points) >= max_turning_points:
                    break
    optimized_path.append(path[-1])
    return optimized_path


def are_points_close(point, points, threshold):
    for p in points:
        dx = abs(point[0] - p[0])
        dy = abs(point[1] - p[1])
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance <= threshold:
            return True
    return False


# Build a KD-tree from the obstacle coordinates
obstacle_kdtree = cKDTree(obstacles)

# Create a QuadTree and insert the obstacles (with buffer zone)
buffered_obstacles = create_buffer_zone(obstacles, buffer_distance)
obstacle_boundary = Boundary(0, 0, GRID_WIDTH, GRID_HEIGHT)
obstacle_quadtree = QuadTree(obstacle_boundary)
for obstacle in buffered_obstacles:
    obstacle_quadtree.insert(obstacle)

min_turning_point_distance = 50  # Adjust this value as needed

# Find the path using A* algorithm
path, _ = astar(start, goal, buffered_obstacles, obstacle_threshold, turning_point_limit)

# Optimize the path by removing unnecessary turning points and limiting the number of turning points
optimized_path = optimize_path(path, turning_point_threshold, obstacle_threshold)

# Post-process the path to remove unnecessary intermediate points
turning_points = []
if path:
    turning_points.append(path[0])  # Start point is always a turning point
    for i in range(1, len(path) - 1):
        current_direction = (path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1])
        next_direction = (path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1])
        if current_direction != next_direction:
            turning_points.append(path[i])
    turning_points.append(path[-1])  # Goal point is always a turning point

# Visualize the grid, obstacles, and path
plt.figure(figsize=(8, 8))
plt.xlim(0, GRID_WIDTH)
plt.ylim(0, GRID_HEIGHT)
plt.title('A* Algorithm - Path Planning')
plt.xlabel('X')
plt.ylabel('Y')


def filter_points(points, threshold):
    filtered_points = []
    for i in range(len(points)):
        current_point = points[i]
        exclude = False
        for j in range(i + 1, len(points)):
            next_point = points[j]
            distance = ((current_point[0] - next_point[0]) ** 2 + (current_point[1] - next_point[1]) ** 2) ** 0.5
            if distance <= threshold:
                exclude = True
                break
        if not exclude:
            filtered_points.append(current_point)
    return filtered_points


filtered_turning_points = filter_points(turning_points, 50)



# Plot the obstacles
for obstacle in obstacles:
    plt.scatter(obstacle[0], obstacle[1], color='red', marker='s', s=80)

# Plot the path if it exists
if path is not None:
    x_path, y_path = zip(*path)
    plt.plot(x_path, y_path, color='blue', linewidth=2, label='Path')
    if filtered_turning_points is not None:
        x_turning, y_turning = zip(*filtered_turning_points)
        plt.scatter(x_turning, y_turning, color='pink', marker='o', s=80, label='Turning Points')
else:
    print('No path found!')

plt.legend()
plt.grid(True)
plt.show()


print(filtered_turning_points)
