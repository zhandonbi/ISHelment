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


@app.route('/add_user/', methods=['POST'])
def AU():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user_age = request.form.get('user_age')
        user_device = request.form.get('user_device')
        return user.add_user(user_name, user_age, user_device)


@app.route('/del_user/', methods=['POST'])
def DU():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        return user.del_user(user_id)


@app.route('/edit_user/', methods=['POST'])
def EU():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        print(request.form)
        message = {
            "name" : request.form.get('user_name'),
            "age" : request.form.get('user_age'),
            "linkNumber" : request.form.get('user_device'),
            "workFinish" : request.form.get('finish_count', type=int),
            "workCount" : request.form.get('all_count',type=int)
        }
        print(message)
        if message['workFinish'] > message['workCount']:
            return user.returnValue(False,'总工作数目低于限定值')
        return user.edit_user(user_id,message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11331)
