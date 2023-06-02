# Class that encapsulates the move into a type and the potential argument that it comes with
# Here speed is only speed
# Argument can be an angle or time
import moveOptions


class MoveClass:
    def __init__(self, my_type, my_speed, my_argument):
        self.type = my_type
        self.speed = my_speed
        self.argument = my_argument

    def print(self):
        print("Move is: " + self.type + ", amount is: " + str(self.speed) + ", Argument is: " + str(self.argument))


def as_payload(dct):
    return MoveClass(dct['type'], dct['speed'], dct['argument'])


# The move function that for now just returns right and 500

def find_move() -> MoveClass:
    move = MoveClass(moveOptions.RIGHT, 500, 100)
    move.print()
    return move
