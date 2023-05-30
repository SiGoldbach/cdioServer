from flask import Flask
import test

app = Flask(__name__)

funString = "HI there"


@app.route('/')
def hello_world():  # put application's code here
    return funString


@app.route('/test')
def fun():
    return test.test_json()


if __name__ == '__main__':
    app.run()
