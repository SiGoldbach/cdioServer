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

p10g = [6, 11]
head10g = [8, 6]
ball10g = [2, 7]
# angle should be -67
print("The angle should be: " + str(Pathfinder.calculate_turn(p10g, head10g, ball10g)))

p11g = [7, 17]
head11g = [13, 20]
ball11g = [2, 14]
# angle should be -175
print("The angle should be: " + str(Pathfinder.calculate_turn(p11g, head11g, ball11g)))

p12g = [7, 17]
head12g = [13, 20]
ball12g = [2, 15]
# angle should be 175
print("The angle should be: " + str(Pathfinder.calculate_turn(p12g, head12g, ball12g)))

p13g = [7, 17]
head13g = [8, 12]
ball13g = [6, 23]
# angle should be 178
print("The angle should be: " + str(Pathfinder.calculate_turn(p13g, head13g, ball13g)))

p14g = [7, 17]
head14g = [8, 12]
ball14g = [8, 23]
# angle should be 159
print("The angle should be: " + str(Pathfinder.calculate_turn(p14g, head14g, ball14g)))

p15g = [7, 17]
head15g = [8, 12]
ball15g = [7, 12]
# angle should be -11
print("The angle should be: " + str(Pathfinder.calculate_turn(p15g, head15g, ball15g)))

p16g = [7, 17]
head16g = [8, 12]
ball16g = [9, 1]
# angle should be -4.2
print("The angle should be: " + str(Pathfinder.calculate_turn(p16g, head16g, ball16g)))

p17g = [7, 17]
head17g = [4, 24]
ball17g = [8, 24]
# angle should be -31
print("The angle should be: " + str(Pathfinder.calculate_turn(p17g, head17g, ball17g)))

p18g = [7, 17]
head18g = [2, 24]
ball18g = [2, 2]
# angle should be 126
print("The angle should be: " + str(Pathfinder.calculate_turn(p18g, head18g, ball18g)))

p19g = [8, 18]
head19g = [2, 18]
ball19g = [8, 2]
# angle should be 90
print("The angle should be: " + str(Pathfinder.calculate_turn(p19g, head19g, ball19g)))

p20g = [8, 18]
head20g = [2, 18]
ball20g = [8, 22]
# angle should be -90
print("The angle should be: " + str(Pathfinder.calculate_turn(p20g, head20g, ball20g)))

p21g = [8, 18]
head21g = [8, 22]
ball21g = [12, 18]
# angle should be -90
print("The angle should be: " + str(Pathfinder.calculate_turn(p21g, head21g, ball21g)))

p22g = [8, 18]
head22g = [8, 22]
ball22g = [12, 18]
# angle should be -90
print("The angle should be: " + str(Pathfinder.calculate_turn(p22g, head22g, ball22g)))

p23g = [8, 18]
head23g = [8, 14]
ball23g = [4, 18]
# angle should be -90
print("The angle should be: " + str(Pathfinder.calculate_turn(p23g, head23g, ball23g)))

p24g = [14, 20]
head24g = [8, 14]
ball24g = [10, 20]
# angle should be -45
print("The angle should be: " + str(Pathfinder.calculate_turn(p24g, head24g, ball24g)))

p25g = [22, 22]
head25g = [8, 14]
ball25g = [18, 22]
# angle should be -30
print("The angle should be: " + str(Pathfinder.calculate_turn(p25g, head25g, ball25g)))
