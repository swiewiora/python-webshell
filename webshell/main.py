from subprocess import PIPE
from traceback import print_exc
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, disconnect
from sarge import Command, Capture
from webshell.set_interval import SetInterval

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True
socket = SocketIO(app)


@app.route('/')
def index():
    return render_template('shell.html')


@socket.on('connect', namespace='/shell')
def connected():
    print('Client connected')


@socket.on('disconnect', namespace='/shell')
def disconnected():
    print('Client disconnected')
    try:
        interval.cancel()
    except NameError:
        print('Interval has not been initialized')
    try:
        process.stdin.close()
        process.stdout.close(True)
        process.stderr.close(True)
        process.kill()
    except NameError:
        print('Process has not been initialized')


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
        disconnect()


@socket.on('command', namespace='/shell')
def command(data):
    cmd = data['msg']
    print(cmd)
    try:
        process.stdin.write(cmd.encode() + b'\n')
        process.stdin.flush()
    except Exception:
        emit('error', {'msg': 'Server operation error'})
        disconnect()
        print_exc()
    stream()


def stream():
    stdout = process.stdout.read().decode()
    stderr = process.stderr.read().decode()
    with app.test_request_context('/'):
        if stdout.strip():
            print(stdout)
            socket.emit('message', {'msg': stdout}, namespace='/shell')
        if stderr.strip():
            print('Process error: ' + stderr)
            socket.emit('error', {'msg': stderr}, namespace='/shell')


def close_process():
    interval.cancel()
    process.stdin.close()
    process.stdout.close(True)
    process.stderr.close(True)
    process.kill()


if __name__ == '__main__':
    socket.run(app)
