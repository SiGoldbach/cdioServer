# I do not know how to make this immutable, do not change this objects state ever
class Field:
    def __init__(self, small_goal, large_goal, obstacle, corners, balls):
        self.small_goal = small_goal
        self.large_goal = large_goal
        self.obstacle = obstacle
        self.corners = corners
        self.balls = balls

    def __str__(self):
        return "The small goal's coordinates: " + str(self.small_goal) + "\n" + "The large goal's coordinates: " + str(
            self.large_goal) + "\n" + "The obstacle has the coordinates: " + str(
            self.obstacle) + "\n" + "The corners have the coordinates: " + str(self.corners) + "\n" + \
               "The balls on the field are located at: " + str(self.balls) + " with len(" + str(len(self.balls)) + ")"
