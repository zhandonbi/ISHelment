from flask import Flask, request, render_template
from flask.helpers import flash
from flask_socketio import SocketIO, emit, send
from werkzeug import debug
from user.user_db import User
from threading import Lock
import random

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def hello_world():
    return render_template('/HW1017_2.html')


@app.route('/find_user_byID/', methods=['POST'])
def FUID():
    if request.method == 'POST':
        user = User()
        id = request.form.get('user_id')
        return user.find_user_by_id(id)


@app.route('/find_user_byName/', methods=['POST'])
def FUN():
    if request.method == 'POST':
        user = User()
        user_name = request.form.get('user_name')
        return user.find_user_by_name(user_name)


@app.route('/add_user/', methods=['POST'])
def AU():
    if request.method == 'POST':
        user = User()
        user_name = request.form.get('user_name')
        user_age = request.form.get('user_age')
        user_device = request.form.get('user_device')
        return user.add_user(user_name, user_age, user_device)


@app.route('/del_user/', methods=['POST'])
def DU():
    if request.method == 'POST':
        user = User()
        user_id = request.form.get('user_id')
        return user.del_user(user_id)


@app.route('/edit_user/', methods=['POST'])
def EU():
    if request.method == 'POST':
        user = User()
        user_id = request.form.get('user_id')
        message = {
            "name": '"{}"'.format(request.form.get('user_name')),
            "age": request.form.get('user_age'),
            "linkNumber": '"{}"'.format(request.form.get('user_device')),
            "workFinish": request.form.get('finish_count', type=int),
            "workCount": request.form.get('all_count', type=int)
        }
        print(message)
        if message['workFinish'] > message['workCount']:
            return user.returnValue(False, '总工作数目低于限定值')
        return user.edit_user(user_id, message)


@app.route('/upload_data/', methods=['POST'])
def UD():
    if request.method == 'POST':
        print(request.args)
        return str(request.args)


@socketio.on('/device_link', namespace='')
def dlu(deviceID):
    print('to device at {}'.format(deviceID))

@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})


@socketio.on('connect', namespace='/manager2')
def handle_my_custom_event2():
    socketio.send('hello',namespace='/manager2')


@socketio.on('connect', namespace='/manager')
def handle_my_custom_event():
    data = {
        'temp': random.randint(0, 100),
        'humi': random.randint(0, 100),
        'yw': False,
        'jsd': '$'.join(random.sample(range(0, 900), 3))
    }
    while True:
        socketio.sleep(5)
        socketio.send(data, True, '/manager')


@socketio.on('disconnect', namespace='/device')
def dsc():
    print('disconnect')


if __name__ == '__main__':
    socketio.run(app=app,
                 host='0.0.0.0',
                 port=11331)
