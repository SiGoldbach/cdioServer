# Use this file for testing the json properties


import MoverFinder
import json
import moveOptions


def test_json():
    move1 = MoverFinder.MoveClass(moveOptions.FORWARD, 500, 400)
    move_as_json = json.dumps(move1.__dict__)
    return move_as_json


json_test = test_json()

print("Json object is: " + json_test)

move = json.loads(json_test, object_hook=MoverFinder.as_payload)

print("Object should now be converted back from json: ")
move.print()
