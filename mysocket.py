import socketio

sio = socketio.Client()

@sio.event
def connect():
    sio.emit('ping', {
        'type': 'pre-cli'
    })
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')

