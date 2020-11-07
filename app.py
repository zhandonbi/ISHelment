from flask import Flask,request
from user.user_db import User

app = Flask(__name__)


@app.route('/')
def hello_world():
    return {
        'status':True,
        'message':'link success'
    }


if __name__ == '__main__':
    app.run(port=8082)
