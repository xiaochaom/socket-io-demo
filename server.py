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
    """

    :param json_str: {"id":"任务执行id","PASS":count, "FAIl":count, "SKIP":count, "TOTAL":count, "STATUS":"任务执行状态,执行中 0,未执行
     1,2 执行完成,3 执行取消"}
    :return:
    """
    print(json_str)
    socket_io.emit('test_client', 'test {}'.format(json_str), namespace='/test')


http_server = WSGIServer(('127.0.0.1', 5000), app, handler_class=WebSocketHandler)
http_server.serve_forever()
