'use strict'

const input = document.getElementById('input')
const shell = document.getElementById('shell')
const converter = document.getElementById('converter')

/**
* Connect to server via SocketIO
*/
const socket = io.connect('http://' + document.domain + ':' + location.port + '/shell')

/**
* Change event listener to 'init'
*/
socket.on('connect', () => {
    status("Connected to server")
    input.removeEventListener('keypress', execute )
    input.addEventListener('keypress', sendShell )
    status("provide path to shell (for example: 'cmd' or '/bin/bash')")
})

socket.on('disconnect', () => {
    status("Disconnected from server")
})

/**
* Convert string to HTML, append to terminal and scroll to the bottom
* @param {string} msg Text to be processed
*/
socket.on('message', (msg) => {
    converter.innerText = msg
    shell.innerHTML += converter.innerHTML
    shell.scrollTop = shell.scrollHeight
})

socket.on('error', error )

socket.on('status', (msg) => { status('Server: ' + msg) } )

/**
* Convert string to HTML, append to terminal surrounded with error tag and scroll to the bottom
* @param {string} mesage Text to be processed
*/
function error(message) {
    converter.innerText = message
    shell.innerHTML += '<error>' + converter.innerHTML + '</error><br />'
    shell.scrollTop = shell.scrollHeight
}

/**
* Convert string to HTML, append to terminal surrounded with i tag and scroll to the bottom
* @param {string} mesage Text to be processed
*/
function status(message) {
    converter.innerText = message
    shell.innerHTML += '<i>' + converter.innerHTML + '</i><br />'
    shell.scrollTop = shell.scrollHeight
}

/**
* Action for event listener, reads content of input field and performs operation
* @param {object} event parameter from EventListener
*/
function execute (event) {
    let code = event.keyCode || event.which
    if (code === 13) {
        let text = input.value
        switch (text) {
            case 'clear':
                shell.innerText = ''
                break
            case '-d':
                socket.disconnect()
                break;
            case '-c':
                socket.connect()
                break;
            default:
                socket.emit('command', text)
                break;
        }

        input.value = ''
    }
}

/**
* Action for event listener, takes path to shell from input fields, sends 'init' message to server,
* changes event listener to 'execute'l
* @param {object} event parameter from EventListener
*/
function sendShell (event) {
    let code = event.mdkeyCode || event.which
    if (code === 13) {
        let text = input.value
        socket.emit('init', text)
        input.value = ''
        input.removeEventListener('keypress', sendShell )
        input.addEventListener('keypress', execute )
    }
}