import math
import MoveTypes
from Moves import MoveClass


def move_to_ball(ball_pos, red_wall_pos):
    x1, y1 = ball_pos
    x2, y2 = red_wall_pos

    # Calculate the midpoint
    midpoint = ((x1 + x2) / 2, (y1 + y2) / 2)

    # Calculate the slope and intercept of the orthogonal line
    if y2 - y1 == 0:
        slope = 0
    else:
        slope = -1 / ((y2 - y1) / (x2 - x1))
    intercept = midpoint[1] - slope * midpoint[0]

    # Calculate the new position on the orthogonal line
    x_new = x1 - 1  # Adjust this value as needed
    y_new = slope * x_new + intercept

    # Calculate the distance and angle to the new position
    delta_x = x_new - x1
    delta_y = y_new - y1
    distance = math.hypot(delta_x, delta_y)
    angle = math.atan2(delta_y, delta_x)

    # Move to the new position
    move = MoveClass(MoveTypes.FORWARD, distance, angle)
    move.print()
    # Perform the movement using your existing move() function
    result = move()  # Adjust this line based on your specific implementation

    # Calculate the distance and angle to the ball
    delta_x = x2 - x_new
    delta_y = y2 - y_new
    distance = math.hypot(delta_x, delta_y)
    angle = math.atan2(delta_y, delta_x)

    # Move towards the ball
    move = MoveClass(MoveTypes.FORWARD, distance, angle)
    move.print()
    # Perform the movement using your existing move() function
    result = move()  # Adjust this line based on your specific implementation
