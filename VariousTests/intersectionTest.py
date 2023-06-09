import math

def calculate_rotation_angles(vector_start, vector_end, target_point):
    xs, ys = vector_start
    xe, ye = vector_end
    xt, yt = target_point

    # Calculate the displacement vectors from start to end and from start to target
    dx1 = xe - xs
    dy1 = ye - ys
    dx2 = xt - xs
    dy2 = yt - ys

    # Calculate the angle between the vectors using dot product
    dot_product = dx1 * dx2 + dy1 * dy2
    magnitude_product = math.hypot(dx1, dy1) * math.hypot(dx2, dy2)

    # Calculate the angle in radians
    angle_rad = math.acos(dot_product / magnitude_product)

    # Calculate the number of angles to rotate
    angles = angle_rad / (math.pi * 2)

    return angles

# Example usage
vector_start = (2, 0)
vector_end = (-2, 0)
target_point = (10, 5)

rotation_angles = calculate_rotation_angles(vector_start, vector_end, target_point)
print("Number of angles to rotate:", rotation_angles)
