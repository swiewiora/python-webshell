const input = document.getElementById('input')
const shell = document.getElementById('shell')
const converter = document.getElementById('converter')
const socket = io.connect('http://' + document.domain + ':' + location.port + '/shell')

socket.on('connect', () => {
    status("Connecting to server")
})

socket.on('disconnect', () => {
    status("Disconnected from server")
})

socket.on('message', (data) => {
    converter.innerText = data.msg + '\n'
    shell.innerHTML += converter.innerHTML
    shell.scrollTop = shell.scrollHeight
})

socket.on('error', (data) => {
    converter.innerText = data.msg
    shell.innerHTML += '<error>' + converter.innerHTML + '</error><br>'
    shell.scrollTop = shell.scrollHeight
})

socket.on('status', (data) => { status('Server: ' + data.msg) } )

function status(message) {
    converter.innerText = message
    shell.innerHTML += '<i>' + converter.innerHTML + '</i><br>'
    shell.scrollTop = shell.scrollHeight
}

input.addEventListener('keypress', (event) => {
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
})

function leave_room() {
    socket.disconnect()
    window.location.href = "http://www.google.com"
}
