import math

import Pathfinder
# I am here making a new formula for calculating a turn I am here using some different tests
# The method seems to work now it is not here anymore only in pathfinder.


p = [382, 130]
head = [306, 102]
ball = [864, 64]
print("The angle should be: " + str(Pathfinder.calculate_turn(p, head, ball)))
# Results should be 151.98
p2 = [8, 6]
head2 = [17, 9]
ball2 = [13, 2]
print("The angle should be: " + str(Pathfinder.calculate_turn(p2, head2, ball2)))
# Results should be -57.09
p3 = [4, 4]
head3 = [10, 6]
ball3 = [6, 10]
print("The angle should be: " + str(Pathfinder.calculate_turn(p3, head3, ball3)))
# Results should be 53.13
p4 = [18, 16]
head4 = [12, 4]
ball4 = [2, 8]
# angle should be 323 or -37
print("The angle should be: " + str(Pathfinder.calculate_turn(p4, head4, ball4)))
p5 = [18, 16]
head5 = [5, 20]
ball5 = [15, 30]
# angle should be 299 or -61
print("The angle should be: " + str(Pathfinder.calculate_turn(p5, head5, ball5)))

p6 = [18, 16]
head6 = [45, 15]
ball6 = [40, 5]
# angle should be 335 or -25
print("The angle should be: " + str(Pathfinder.calculate_turn(p6, head6, ball6)))

p7 = [18, 16]
head7 = [15, 5]
ball7 = [30, 10]
# angle should be 79 or 279
print("The angle should be: " + str(Pathfinder.calculate_turn(p7, head7, ball7)))

p8 = [3, 3]
head8 = [1, 6]
ball8 = [2, 7]
# angle should be -20
print("The angle should be: " + str(Pathfinder.calculate_turn(p8, head8, ball8)))

p9 = [3, 3]
head9 = [4, 6]
ball9 = [2, 7]
# angle should be 32
print("The angle should be: " + str(Pathfinder.calculate_turn(p9, head9, ball9)))

p10 = [2, -4]
head10 = [6, -2]
ball10 = [8, -6]
# angle should be -45
print("The angle should be: -45 and is: " + str(Pathfinder.calculate_turn(p10, head10, ball10)))


p11 = [3, 3]
head11 = [4, 6]
ball11 = [2, 7]
# angle should be 32
print("The angle should be: " + str(Pathfinder.calculate_turn(p11, head11, ball11)))
