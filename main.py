#!/usr/bin/env python

from subprocess import check_output, PIPE, Popen
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
# from flask_login import current_user

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
    process = Popen('cmd', shell=True, stdin=PIPE, stdout=PIPE)
    emit('status', {'msg': 'Connected to server'})


@socketio.on('command', namespace='/shell')
def command(cmd):
    message = cmd['msg']
    emit('message', {'msg': '$ ' + message})
    message = (message + '\r\n').encode()
    print(message)
    try:
        # process.stdin.write(message.encode() + b'\n')
        # process.stdin.flush()
        (stdout, stderr) = process.communicate(input=message, timeout=30)
        print(stdout)
        print(stderr)
        exitstatus = process.poll()
        if exitstatus == 0:
            emit('message', {'msg': stdout.decode()})
        else:
            emit('error', {'msg': stderr.decode()})
    except Exception as err:
        result = str(err)
        print(result)
        emit('error', {'msg': result})


if __name__ == '__main__':
    socketio.run(app, debug=True)
