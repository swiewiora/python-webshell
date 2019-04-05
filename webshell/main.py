from subprocess import PIPE
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, disconnect
from traceback import print_exc, print_exception
from sarge import Command, Capture
from webshell.set_interval import SetInterval
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True
Bootstrap(app)
socket = SocketIO(app)


@app.route('/')
def index():
    return render_template('shell.html')

#
# @socket.on('connect', namespace='/shell')
# def connected():
#     emit('status', {'msg': 'Connected to server'})


@socket.on('disconnect', namespace='/shell')
def disconnected():
    print('Client disconnected')
    if interval:
        interval.cancel()
    if process:
        process.stdin.close()
        process.stdout.close(True)
        process.stderr.close(True)
        process.kill()


@socket.on('init', namespace='/shell')
def init(data):
    shell = data['msg']
    global process
    process = Command(shell,
                      stdout=Capture(buffer_size=-1),
                      stderr=Capture(buffer_size=-1),
                      )
    try:
        process.run(input=PIPE, async_=True)
        global interval
        interval = SetInterval(1, stream)
    except ValueError as exception:
        print_exc()
        emit('error', {'msg': str(exception)})
        emit('error', {'msg': 'Initialization failed'})
        close_process()
        disconnect()


@socket.on('command', namespace='/shell')
def command(data):
    cmd = data['msg']
    emit('message', {'msg': '$ ' + cmd})
    print(cmd)
    process.stdin.write(cmd.encode() + b'\n')
    process.stdin.flush()
    stream()


def stream():
    stdout = process.stdout.read().decode()
    stderr = process.stderr.read().decode()
    print(stdout)
    print_exception(Exception, stderr)
    emit('message', {'msg': stdout})
    emit('error', {'msg': stderr})


def close_process():
    interval.cancel()
    process.stdin.close()
    process.stdout.close(True)
    process.stderr.close(True)
    process.kill()


if __name__ == '__main__':
    socket.run(app, debug=True)
