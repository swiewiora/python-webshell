# Python Web Shell
The purpose of this project was to create a web application in Python which will allow the user to execute arbitrary 
shell commands on the remote web server via a browser.

The application provides the user with a text box where they will enter the commands. The commands shall be 
sent to the server. The server executes the commands in a shell sub-process, capture standard and error output and 
send it back to the browser, which displays it (e.g. using different colours for standard and error output, 
respectively).
------------
## Install

Create a virtualenv (Python 3 built-in venv) and (optionally) activate it:

    python -m venv venv
    . venv/bin/activate

Or on Windows cmd:

    python -m venv venv
    venv\Scripts\activate.bat

Install WebShell:

    pip install . -r requirements.txt

## Run

    export FLASK_APP=webshell
    flask run
Or on Windows cmd:

    set FLASK_APP=webshell
    flask run
Open http://localhost:5000 in a browser.

## Debugging

    FLASK_APP=webshell
    FLASK_DEBUG=true
    flask run --no-reload

or execute main script

    python main.py
## Resources
- [Flask](http://flask.pocoo.org)
- [Flask-SocketIO](http://flask-socketio.readthedocs.io/en/latest/)
- [Socket.IO](https://socket.io/)