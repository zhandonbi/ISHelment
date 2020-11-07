from flask import Flask, request
from user.user_db import User

app = Flask(__name__)
user = User()


@app.route('/')
def hello_world():
    return {'status': True, 'message': 'link success'}


@app.route('/find_user_byID/', methods=['POST'])
def FUID():
    if request.method == 'POST':
        id = request.form.get('user_id')
        return user.find_user_by_id(id)


@app.route('/find_user_byName/', methods=['POST'])
def FUN():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        return user.find_user_by_name(user_name)


@app.route('/add_user/')
def AU():
    if request.method == 'POST':
        user_name = request.get('user_name')
        user_age = request.get('user_age')
        user_device = request.get('user_device')
        return user.add_user(user_name, user_age, user_device)


@app.route('/del_user/')
def DU():
    if request.method == 'POST':
        user_id = request.get('user_id')
        return user.del_user(user_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
