import math
import MoveTypes
from Moves import MoveClass


def move_to_ball(ball_pos, red_wall_pos, boundary_distance=10):
    # Calculate the orthogonal line parameters
    x1, y1 = ball_pos
    x2, y2 = red_wall_pos

    midpoint = ((x1 + x2) / 2, (y1 + y2) / 2)

    if y2 - y1 == 0:
        slope = 0
    else:
        slope = -1 / ((y2 - y1) / (x2 - x1))

    intercept = midpoint[1] - slope * midpoint[0]

    # Calculate the new position on the orthogonal line
    x_new = x1 - 1  # Adjust this value as needed
    y_new = slope * x_new + intercept

    # Calculate the distance and angle to the new position
    distance = math.sqrt((x_new - x1) ** 2 + (y_new - y1) ** 2)
    angle = math.atan2(y_new - y1, x_new - x1)

    # Check if the distance is within the boundary
    if distance > boundary_distance:
        # Move to the new position
        move = MoveClass(MoveTypes.FORWARD, distance, angle)
        move.print()
        # Perform the movement using your existing move() function
        result = move()  # Adjust this line based on your specific implementation

    # Calculate the distance and angle to the ball
    distance = math.sqrt((x2 - x_new) ** 2 + (y2 - y_new) ** 2)
    angle = math.atan2(y2 - y_new, x2 - x_new)

    # Move towards the ball
    move = MoveClass(MoveTypes.FORWARD, distance, angle)
    move.print()
    # Perform the movement using your existing move() function
    result = move()  # Adjust this line based on your specific implementation
