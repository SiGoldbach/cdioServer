import math
import math

import math


def calculate_center_angle(vector_start_x, vector_start_y, vector_end_x, vector_end_y, target_x, target_y):
    # Calculate the midpoint of the vector
    midpoint_x = (vector_start_x + vector_end_x) / 2
    midpoint_y = (vector_start_y + vector_end_y) / 2

    # Calculate the angle between the vector and the line connecting the midpoint to the target ball
    vector_angle = math.atan2(vector_end_y - vector_start_y, vector_end_x - vector_start_x)
    target_angle = math.atan2(target_y - midpoint_y, target_x - midpoint_x)

    # Calculate the center angle
    center_angle = math.atan2(math.sin(vector_angle) + math.sin(target_angle),
                              math.cos(vector_angle) + math.cos(target_angle))

    return center_angle


# Example usage
vector_start_x = 4
vector_start_y = -8
vector_end_x = 5
vector_end_y = -6
target_x = 1
target_y = -1

center_angle = calculate_center_angle(vector_start_x, vector_start_y, vector_end_x, vector_end_y, target_x, target_y)

print("Center Angle:", math.degrees(center_angle))


def determine_turn_direction(vector_start_x, vector_start_y, vector_end_x, vector_end_y, target_x, target_y):
    # Calculate the vector from the starting point of your vector to the target point
    target_vector_x = target_x - vector_start_x
    target_vector_y = target_y - vector_start_y

    # Calculate the cross product
    cross_product = (vector_end_x - vector_start_x) * target_vector_y - (
            vector_end_y - vector_start_y) * target_vector_x

    # Determine the direction of the turn
    if cross_product > 0:
        turn_direction = "left"
    else:
        turn_direction = "right"

    return turn_direction


# Example usage
vector_start_x = 4
vector_start_y = -8
vector_end_x = 5
vector_end_y = -6
target_x = 1
target_y = -1
turn_direction = determine_turn_direction(vector_start_x, vector_start_y, vector_end_x, vector_end_y, target_x,
                                          target_y)

print("Turn", turn_direction)

