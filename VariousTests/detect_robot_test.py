import detectRobot
import detectField

front, back = detectRobot.detect_robot()

print("The front of the robot was found as: ", front)
print("The back of the robot was found as: ", back)
