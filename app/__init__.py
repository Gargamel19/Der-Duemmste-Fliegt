from flask import Flask

from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

chat_reader = None

from app import routes