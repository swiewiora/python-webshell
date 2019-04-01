importScripts('https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.dev.js');
let socket = null

debugger
self.onmessage = (event) => {
debugger
//     let port = event.ports[0]

    if (event.data == 'start') {
        if (!socket) {
            socket = io.connect('http://127.0.0.1:5000/shell')
                socket.on('connect', () => {
                socket.emit('joined', {})
            })

            socket.on('message', message)

            socket.on('error', (data) => {
                data = JSON.stringify({ type: 'error', msg: data.msg })
                postMessage(data)
            })

            socket.on('status', (data) => {
                data = JSON.stringify({ type: 'status', msg: data.msg })
                postMessage(data)
            })
        } else {
            let text = "Reusing current connection"
            let data = JSON.stringify({ type: 'status', msg: text})
            postMessage(data)
        }
    } else {
        let data = JSON.parse(event.data)
        switch (data.type) {
            case 'command':
                socket.emit('command', {msg: data.msg})
                break
        } 
    }
}

function message(data) {
    data = JSON.stringify({ type: 'message', msg: data.msg })
    postMessage(data)
}

function leave_room() {
    socket.disconnect()
//     window.location.href = "http://www.google.com"
}