from app import app, socketio

if __name__ == '__main__':

	# app.run(host='0.0.0.0', debug=True, port=6500, use_reloader=False)
	socketio.run(app, host='0.0.0.0', port=6500, debug=True, use_reloader=False)
