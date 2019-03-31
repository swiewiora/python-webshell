const socket = io.connect('http://' + document.domain + ':' + location.port + '/shell')
const input = document.getElementById('input')
const shell = document.getElementById('shell')

socket.on('connect', function() {
    socket.emit('joined', {})
});

socket.on('message', function(data) {
    shell.value = shell.value + data.msg + '\n'
    shell.scrollTop = shell.scrollHeight
});

socket.on('status', function(data) {
    shell.value = shell.value + '<' + data.msg + '>\n'
    shell.scrollTop = shell.scrollHeight
});

input.addEventListener('keypress', (event) => {
    let code = event.keyCode || event.which
    if (code == 13) {
        text = input.value
        socket.emit('command', {msg: text})
        input.value = ''
    }
})

function leave_room() {
    socket.disconnect()
    window.location.href = "http://www.google.com"
}