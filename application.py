#!/usr/bin/env python

import subprocess
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask('webshell')
app.config['SECRET_KEY'] = 'top secret'
app.config['DEBUG'] = True
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('shell.html')


@socketio.on('joined', namespace='/shell')
def joined(message):
    emit('status', {'msg': 'Connected to server'})


@socketio.on('command', namespace='/shell')
def command(cmd):
    c = cmd['msg']
    emit('message', {'msg': '$ ' + c})
    print(c)
    try:
        result = subprocess.check_output(c, shell=True).decode()
        emit('message', {'msg': result})
    except Exception as err:
        result = str(err)
        emit('error', {'msg': result})


if __name__ == '__main__':
    socketio.run(app)