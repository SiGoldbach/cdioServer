from flask import Flask
import test
# import Image
# import Pathfinding

app = Flask(__name__)

funString = "HI there"


@app.route('/')
def hello_world():  # put application's code here
    return funString


@app.route('/test')
def fun():
    # Image.calculate_move()
    return test.test_json()


if __name__ == '__main__':
    app.run()
