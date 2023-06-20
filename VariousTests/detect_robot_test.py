import detectRobot
import detectField

front, back = detectField.detect_field()

print("The front of the robot was found as: ", front)
print("The back of the robot was found as: ", back)
