# I do not know how to make this immutable, do not change this objects state ever
class State:
    def __init__(self, small_goal, large_goal, obstacle, corners, balls, mode, need_new_detect_balls, goal_ball,
                 ball_amount_guess, non_delivered_balls, robot_delivery_location_small):
        self.small_goal = small_goal
        self.large_goal = large_goal
        self.obstacle = obstacle
        self.corners = corners
        self.balls = balls
        self.mode = mode
        self.need_new_detect_balls = need_new_detect_balls
        self.goal_ball = goal_ball
        self.ball_amount_guess = ball_amount_guess
        self.non_delivered_balls = non_delivered_balls
        self.robot_delivery_location_small = robot_delivery_location_small

    def __str__(self):
        return "The small goal's coordinates: " + str(self.small_goal) + "\n" + "The large goal's coordinates: " + str(
            self.large_goal) + "\n" + "The obstacle has the coordinates: " + str(
            self.obstacle) + "\n" + "The corners have the coordinates: " + str(self.corners) + "\n" + \
               "The balls on the field are located at: " + str(self.balls) + " with len(" + str(
            len(self.balls)) + ")\n" + "If the robot where to deliver the balls to the small goal it should go here" + \
               str(self.robot_delivery_location_small)
