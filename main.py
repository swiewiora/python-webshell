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
    global process
    process = Popen('cmd',  # await?
                    shell=True,  # security hazard
                    stdin=PIPE,
                    stdout=PIPE,
                    stderr=PIPE
                    )
    while True:
        try:
            print(process.stdout.readline())
        except Exception as err:
            print("execption: " + str(err) )
            break

    emit('status', {'msg': 'Connected to server'})


@socketio.on('command', namespace='/shell')
def command(cmd):
    message = cmd['msg']
    emit('message', {'msg': '$ ' + message})
    print(message)
    message = (message + '\r\n').encode()
    # try:

    process.stdin.write(message)
    process.stdin.flush()
    # process.wait()

    stdout = process.stdout.readline()

    # stderr = process.stderr.readlines()
    print(stdout, stderr)

    process.stdout.flush()
    process.stderr.flush()

    # (stdout, stderr) = process.communicate()
    # exitstatus = process.poll()
    if stdout:
        emit('message', {'msg': stdout})
    if stderr:
        emit('error', {'msg': stderr})
    # except Exception as err:
    #     result = str(err)
    #     print(result)
    #     emit('error', {'msg': result})


if __name__ == '__main__':
    socketio.run(app, debug=True)
