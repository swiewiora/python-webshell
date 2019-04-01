#!/usr/bin/env python

from subprocess import check_output, PIPE, Popen
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_login import current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('shell.html')


@socketio.on('joined', namespace='/shell')
def joined(msg):
    # Run "cat", which is a simple Linux program that prints it's input.
    global process
    process = Popen(shell=True, stdin=PIPE, stdout=PIPE)
    emit('status', {'msg': 'Connected to server'})


@socketio.on('command', namespace='/shell')
def command(cmd):
    command = cmd['msg']
    emit('message', {'msg': '$ ' + command})
    print(command)
    try:
        process.stdin.write(b'cd ..\n')
        process.stdin.flush()
        output = process.stdout.read()
        exitstatus = process.poll()
        if exitstatus == 0:
            emit('message', {'msg': output})
        else:
            emit('error', {'msg': output})

    except Exception as err:
        result = str(err)
        emit('error', {'msg': result})




if __name__ == '__main__':
    socketio.run(app, debug=True)
