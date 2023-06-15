import time

import MoveTypes
import Moves
import Pathfinder
import detectBalls
import detectField
import State
import robot_modes

# Sleeping to make sure camera is focused before taking picture of the field to get better camera quality
time.sleep(2)

print("Video quality has been increased and the program have slept 5 seconds to focus")
smallGoal, bigGoal, obstacle, corners = detectField.detect_field()
balls = detectBalls.detect_balls()
state = State.State(smallGoal, bigGoal, obstacle, corners, balls, robot_modes.COLLECT, False)
print(state.__str__())


# As for right now this function just returns the tiniest turn just to make sure the client does not crash
# Now there is a check here if the robot needs to try and collect the balls or try to deliver the balls
def calculate_move():
    if state.robot_just_drove:
        updated_ball_state = detectBalls.detect_balls()
        state.balls = updated_ball_state
    if state.mode == robot_modes.COLLECT:
        return Pathfinder.collect_balls(state)
    elif state.mode == robot_modes.DELIVER:
        return Pathfinder.deliver_balls(state)
    else:
        return Moves.MoveClass(MoveTypes.TURN, 500, 5)

# move = calculate_move()
# move.print()
