from flask import Flask
# LiveVideoFeed is being initialized here so the rather long start up process start as early as possible
# The app then calls the live video feeds method calculate move since it has the video-feed,
# and therefore can give the video feed to the pathfinder as a middle man
import ServerInitializer
import json

import MoveTypes
import Moves

app = Flask(__name__)

funString = "HI there"


@app.route('/')
def hello_world():  # put application's code here
    move1 = Moves.MoveClass(MoveTypes.TURN, 90, 90)
    move_as_json = json.dumps(move1.__dict__)
    return move_as_json


@app.route('/test')
def fun():
    # Image.calculate_move()
    move1 = ServerInitializer.calculate_move()
    if move1 is None:
        print("Move to return is none")
        #Now if the move is none something will get returned to the function
        return json.dumps(Moves.MoveClass(MoveTypes.TURN, 500, 10).__dict__)

    move_as_json = json.dumps(move1.__dict__)
    return move_as_json
    # except AttributeError:
    # print("No Json move was returned ")
    # return json.dumps(Moves.MoveClass(MoveTypes.ERROR, 500, -50).__dict__)


@app.route('/get_command')
def command():
    return ServerInitializer.calculate_move()


if __name__ == '__main__':
    app.run()
