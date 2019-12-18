from logging.config import dictConfig

from flask import Flask, request
from flask_socketio import SocketIO
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

app = Flask(__name__)
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    }
})
socket_io = SocketIO(app, cors_allowed_origins="*")


@socket_io.on('connect', namespace='/test')
def connect():
    print('connect done! {}'.format(request.sid))


@socket_io.on('test_server', namespace='/test')
def test_server(json_str):

    print(json_str)
    socket_io.emit('test_client', 'test {}'.format(json_str), namespace='/test')


http_server = WSGIServer(('127.0.0.1', 5000), app, handler_class=WebSocketHandler)
http_server.serve_forever()
