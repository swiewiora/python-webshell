const input = document.getElementById('input')
const shell = document.getElementById('shell')
const socket = io.connect('http://' + document.domain + ':' + location.port + '/shell')

socket.on('connect', () => {
    socket.emit('joined', {})
})

socket.on('message', (data) => {
    shell.innerText += data.msg + '\n'
    shell.scrollTop = shell.scrollHeight
})

socket.on('error', (data) => {
    shell.innerHTML += '<error>' + data.msg + '</error><br>'
    shell.scrollTop = shell.scrollHeight
})

socket.on('status', (data) => {
    shell.innerText += '<' + data.msg + '>\n'
    shell.scrollTop = shell.scrollHeight
})

input.addEventListener('keypress', (event) => {
    let code = event.keyCode || event.which
    if (code === 13) {
        text = input.value
        if (text === 'clear' ) {
            shell.innerText = ' '
        } else {
            socket.emit('command', {msg: text})
            input.value = ''
        }

    }
})

function leave_room() {
    socket.disconnect()
    window.location.href = "http://www.google.com"
}