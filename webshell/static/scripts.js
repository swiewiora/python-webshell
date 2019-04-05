const input = document.getElementById('input')
const shell = document.getElementById('shell')
const converter = document.getElementById('converter')

const socket = io.connect('http://' + document.domain + ':' + location.port + '/shell')

socket.on('connect', () => {
    status("Connected to server")
    input.removeEventListener('keypress', execute(event) )
    input.addEventListener('keypress', sendShell(event) )
    status("provide path to the shell")
})

socket.on('disconnect', () => {
    status("Disconnected from server")
})

socket.on('message', (data) => {
    converter.innerText = data.msg + '\n'
    shell.innerHTML += converter.innerHTML
    shell.scrollTop = shell.scrollHeight
})

socket.on('error', (data) => { error(data.msg) } )

socket.on('status', (data) => { status('Server: ' + data.msg) } )

function error(message) {
    converter.innerText = message
    shell.innerHTML += '<error>' + converter.innerHTML + '</error><br>'
    shell.scrollTop = shell.scrollHeight
}

function status(message) {
    converter.innerText = message
    shell.innerHTML += '<i>' + converter.innerHTML + '</i><br>'
    shell.scrollTop = shell.scrollHeight
}

function execute (event) {
    let code = event.keyCode || event.which
    if (code === 13) {
        text = input.value
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
                socket.emit('command', {msg: text})
                break;
        }

        input.value = ''
    }
}

function sendShell (event) {
    let code = event.keyCode || event.which
    if (code === 13) {
        text = input.value
        socket.emit('init', {msg: text})
        input.value = ''
        input.removeEventListener('keypress', sendShell(event) )
        input.addEventListener('keypress', execute(event) )
    }
}