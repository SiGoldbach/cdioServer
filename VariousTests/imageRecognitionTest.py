import cv2 as cv
import ImFromPhoto
import VectorTest

image = cv.imread('../Resources/Pictures/withBall3.jpg')

balls, robot = ImFromPhoto.imageRecognition(image)
print("Result from test: ")
print(balls)
print(robot)
print(len(balls))
# Trying the vectorTest
x = VectorTest.determine_turn_direction(int(robot[1][0]), -int(robot[1][1]), int(robot[0][0]), -int(robot[0][1]),
                                        int(balls[0][0]), -int(balls[0][1]))
print(x)
y = VectorTest.calculate_center_angle(int(robot[1][0]), -int(robot[1][1]), int(robot[0][0]), -int(robot[0][1]),
                                      int(balls[0][0]), -int(balls[0][1]))
print(y)
