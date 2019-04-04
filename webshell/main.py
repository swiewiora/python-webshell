from subprocess import check_output
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import traceback
from sarge import Command, Capture
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True
socket = SocketIO(app)


@app.route('/')
def index():
    return render_template('shell.html')


@socket.on('connect', namespace='/shell')
def connected():
    emit('status', {'msg': 'Connected to server'})


@socket.on('disconnect', namespace='/shell')
def disconnected():
    print('Client disconnected')



@socket.on('command', namespace='/shell')
def command(data):
    cmd = data['msg']
    emit('message', {'msg': '$ ' + cmd})
    print(cmd)
    try:
        result = check_output(cmd, shell=True, universal_newlines=True)
        emit('message', {'msg': result})
    except Exception as err:
        traceback.print_exc()
        result = str(err)
        emit('error', {'msg': result})


if __name__ == '__main__':
    socket.run(app, debug=True)
