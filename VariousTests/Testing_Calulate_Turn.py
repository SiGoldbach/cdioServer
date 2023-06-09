import math

import Pathfinder

# turn = Pathfinder.calculate_turn([2, 3], [0, 0], [6, 1])
# I am here making a new formula for calculating a turn I am here using some different tests
# The method seems to work now it is not here anymore only in pathfinder.


p = [382, 130]
head = [306, 102]
ball = [864, 64]
print("The angle should be: " + str(Pathfinder.angle_good(p, head, ball)))
p2 = [8, 6]
head2 = [17, 9]
ball2 = [13, 2]
print("The angle should be: " + str(Pathfinder.angle_good(p2, head2, ball2)))
