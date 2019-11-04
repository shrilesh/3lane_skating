from flask import Flask, render_template
from flask_mongokit import MongoKit
from flask_socketio import SocketIO, emit, send, join_room
from flask_cors import CORS
from bson import json_util
import json,eventlet,greenlet,gevent
from gevent import monkey
monkey.patch_all()



app = Flask(__name__)

socketio = SocketIO(app,async_mode="threading")

@socketio.on('connect', namespace="/display")
def handle_connect():
	join_room('display_room')
	send(json.dumps({
		"message": "Connected Successfully",
		"type": "message"
		}, default=json_util.default))

CORS(app)

app.config.from_object('conf.mainconf.DevelopmentConfig')

db = MongoKit(app)

import api