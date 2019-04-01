#!/usr/bin/env python

import os
from subprocess import check_output
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('shell.html')


@socketio.on('joined', namespace='/shell')
def joined(msg):
    emit('status', {'msg': 'Connected to server'})


@socketio.on('command', namespace='/shell')
def command(cmd):
    c = cmd['msg']
    emit('message', {'msg': '$ ' + c})
    print(c)
    try:
        result = check_output(c, shell=True).decode()
        emit('message', {'msg': result})
    except Exception as err:
        result = str(err)
        emit('error', {'msg': result})


# @app.route('/js/<path:filename>')
# def send_js(filename):
#     root_dir = os.path.dirname(os.getcwd())
#     return send_from_directory(os.path.join('.', 'static', 'js'), filename)


if __name__ == '__main__':
    socketio.run(app, debug=True)
