import asyncio

import socketio

sio = socketio.Client()


@sio.event(namespace='/test')
def connect():
    print('connection established')
    sio.emit('test_server', "test", namespace='/test')


@sio.event(namespace='/test')
def test_client(t):
    print(t)
    sio.emit('test_server', "test", namespace='/test')


sio.connect('http://localhost:5000', namespaces='/test')
sio.wait()

# sio = socketio.AsyncClient()
#
#
# @sio.event(namespace='/test')
# async def connect():
#     print('connection established')
#     await sio.emit('test_server', "test", namespace='/test')
#
#
# @sio.event(namespace='/test')
# async def test_client(t):
#     print(t)
#     await sio.emit('test_server', "test", namespace='/test')
#
#
# async def start_server():
#     await sio.connect('http://localhost:5000', namespaces='/test')
#     await sio.wait()
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(start_server())
