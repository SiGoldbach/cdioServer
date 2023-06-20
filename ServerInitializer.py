import time

import MoveTypes
import Moves
import Pathfinder
import detectBalls
import detectField
import State
import robot_modes


smallGoal, bigGoal, obstacle, corners = detectField.detect_field()
balls = detectBalls.detect_balls()
state = State.State(small_goal=smallGoal, large_goal=bigGoal, obstacle=obstacle, corners=corners, balls=balls,
                    mode=robot_modes.COLLECT,
                    need_new_detect_balls=False,
                    goal_ball=None, ball_amount_guess=0, non_delivered_balls=len(balls),
                    robot_delivery_location_small=(smallGoal[0] + 200, smallGoal[1]),
                    robot_delivery_location_big=(bigGoal[0] - 200, bigGoal[1]),
                    delivery_mode=robot_modes.AT_RANDOM_PLACE, big_or_small_goal=robot_modes.SMALL_GOAL)
print(state.__str__())


# As for right now this function just returns the tiniest turn just to make sure the client does not crash
# Now there is a check here if the robot needs to try and collect the balls or try to deliver the balls
def calculate_move():
    if state.need_new_detect_balls:
        updated_ball_state = detectBalls.detect_balls()
        if updated_ball_state is None:
            state.mode = robot_modes.DELIVER
        state.balls = updated_ball_state
    if state.mode == robot_modes.COLLECT:
        return Pathfinder.collect_balls(state)
    elif state.mode == robot_modes.DELIVER:
        return Pathfinder.deliver_balls(state)
    else:
        return Moves.MoveClass(MoveTypes.TURN, 500, 5)

# move = calculate_move()
# move.print()
