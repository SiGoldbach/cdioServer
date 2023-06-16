import detectField

smallGoal, bigGoal, obstacle, walls = detectField.detect_field()
print("The big goal was found as: ", bigGoal)
print("The small goal was found as: ", smallGoal)
print("The walls where found as: ", walls)
print("The obstacle was found as: ", obstacle)
