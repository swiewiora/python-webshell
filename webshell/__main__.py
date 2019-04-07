from subprocess import PIPE
from flask import Flask, render_template
# print catched exceptions to the log
from traceback import print_exc
# send and receive messages with client
from flask_socketio import SocketIO, emit, disconnect
# use subprocess avoiding deadlocks
from sarge import Command, Capture
# send shell output to client in a fixed intervals
from webshell.set_interval import SetInterval

app = Flask(__name__)  # Init Flask app
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True
socket = SocketIO(app)  # Include SocketIO


@app.route('/')
def index():
    return render_template('shell.html')


@socket.on('connect', namespace='/shell')
def connected():
    print('Client connected')


@socket.on('disconnect', namespace='/shell')
def disconnected():
    """Cancel interval, close IO streams, kill subprocess"""
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
def init(shell):
    """"Run arbitrary shell in subprocess asynchronously,
    Sets read stdout and stderr in intervals,
    Sets global variables: process and interval.
    If the path is incorrect, disconnect client.

    :param shell: path to arbitrary shell to run
    :type shell: str
    """
    global process
    process = Command(shell,
                      stdout=Capture(buffer_size=-1),
                      stderr=Capture(buffer_size=-1),
                      )
    try:
        process.run(input=PIPE, async_=True)  # run arbitrary shell
        global interval
        interval = SetInterval(1, stream)  # Schedule intervals
    except ValueError as exception:  # incorrect shell path
        print_exc()
        emit('error', str(exception))
        emit('error', 'Initialization failed')
        disconnect()


@socket.on('command', namespace='/shell')
def command(cmd):
    """"Send command to sub-process. On any exception, disconnect client
    and kill sub-process.

    :param cmd: Input command
    :type cmd: str
    """
    print(cmd)
    try:
        process.stdin.write(cmd.encode() + b'\n')
        process.stdin.flush()
    except Exception:
        emit('error', 'Server operation error')
        disconnect()
        print_exc()
    stream()


def stream():
    """"Read standard and error output from sub-process and send to client."""
    stdout = process.stdout.read().decode()
    stderr = process.stderr.read().decode()
    with app.test_request_context('/'):
        if stdout.strip():
            print(stdout)
            socket.emit('message', stdout, namespace='/shell')
        if stderr.strip():
            print('Process error: ' + stderr)
            socket.emit('error', stderr, namespace='/shell')


if __name__ == '__main__':
    socket.run(app)
