import math

import Pathfinder


# turn = Pathfinder.calculate_turn([2, 3], [0, 0], [6, 1])
# I am here making a new formula for calculating a turn I am here using some different tests

def angle(p1, head1, ball1):
    m1 = (head1[1] - p1[1]) / (head1[0] - p1[0])
    m2 = (ball1[1] - p1[1]) / (ball1[0] - p1[0])
    angle_cal = math.atan((m2 - m1) / (1 + m1 * m2)) * 180 / math.pi

    # Here the function needs to check the quadrant of the angle

    if head[0] - p[0] < 0:
        angle_cal += 180
    elif ball[0] - p[0] < 0:
        angle_cal += 180
    return angle_cal


p = [382, 130]
head = [306, 102]
ball = [864, 64]
print("The angle should be: " + str(angle(p, head, ball)))
p2 = [8, -6]
head2 = [17, -9]
ball2 = [13, -2]
print("The angle should be: " + str(angle(p2, head2, ball2)))
