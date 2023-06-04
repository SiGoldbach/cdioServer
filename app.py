from flask import Flask

# LiveVideoFeed is being initialized here so the rather long start up process start as early as possible
# The app then calls the live video feeds method calculate move since it has the video-feed,
# and therefore can give the video feed to the pathfinder as a middle man
import LiveVideoFeed
import json

app = Flask(__name__)

funString = "HI there"


@app.route('/')
def hello_world():  # put application's code here
    return funString


@app.route('/test')
def fun():
    # Image.calculate_move()
    move1 = LiveVideoFeed.calculate_move()
    move_as_json = json.dumps(move1.__dict__)
    return move_as_json


@app.route('/get_command')
def command():
    return LiveVideoFeed.calculate_move()


if __name__ == '__main__':
    app.run()
