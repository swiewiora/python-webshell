const input = document.getElementById('input')
const shell = document.getElementById('shell')

if (!window.SharedWorker) {
    console.log("SharedWorker not supported")
}

var worker = new SharedWorker('/static/js/sharedSockets.js')
//worker.port.start()
//worker.port.postMessage("start")

worker.port.onmessage = (event) => {
    let data = JSON.parse(event.data)
    switch (data.type) {
        case 'message':
            shell.innerText += data.msg + '\n'
            shell.scrollTop = shell.scrollHeight
            break
        case 'error':
            shell.innerHTML += '<error>' + data.msg + '</error><br>'
            shell.scrollTop = shell.scrollHeight
            break
        case 'status':
            shell.innerText += '< ' + data.msg + ' >\n'
            break
    }
    shell.scrollTop = shell.scrollHeight
}

worker.onerror = () => {
    console.log('There is an error with your worker!');
}

input.addEventListener('keypress', (event) => {
    let code = event.keyCode || event.which
    if (code === 13) {
        text = input.value
        if (text === 'clear' ) {
            shell.innerText = ''
        } else {
            let data = JSON.stringify({ type: 'command', msg: text})
            worker.port.postMessage(data)
            input.value = ''
        }
    }
})

