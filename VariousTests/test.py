# Use this file for testing serialization
# this file can also be used if one wants to send the same command over and over to the robot


import Moves
import json
import MoveTypes


def test_json():
    move1 = Moves.MoveClass(MoveTypes.LEFT, 500, 2057)
    move_as_json = json.dumps(move1.__dict__)
    return move_as_json


json_test = test_json()

print("Json object is: " + json_test)

move = json.loads(json_test, object_hook=Moves.as_payload)

print("Object should now be converted back from json: ")
move.print()
