from flask import Flask

app = Flask(__name__)

funString = "HI there"


@app.route('/')
def hello_world():  # put application's code here
    return funString


if __name__ == '__main__':
    app.run()
