from flask import Response, render_template, request
from app import app, db, socketio
from bson import json_util
import os
import json

@app.route('/timer_display', methods=['GET'])
def display():
    return render_template("skating.html")

