#!/usr/bin/env python

from subprocess import check_output
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import traceback

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('shell.html')


@socketio.on('connect', namespace='/shell')
def connected():
    emit('status', {'msg': 'Connected to server'})


@socketio.on('disconnect', namespace='/shell')
def disconnected():
    print('Client disconnected')


@socketio.on('command', namespace='/shell')
def command(cmd):
    command = cmd['msg']
    emit('message', {'msg': '$ ' + command})
    print(command)
    try:
        result = check_output(command, shell=True, universal_newlines=True) #.decode()
        emit('message', {'msg': result})
    except Exception as err:
        traceback.print_exc()
        result = str(err)
        emit('error', {'msg': result})


if __name__ == '__main__':
    socketio.run(app, debug=True)
