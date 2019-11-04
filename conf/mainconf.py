from flask import Config
import os

class DevelopmentConfig(Config):


	MONGODB_DATABASE = "three_lane_db"
	MONGODB_HOST = "127.0.0.1"
	MONGODB_PORT = 27017
	MONGODB_USERNAME = "three_lane_user"
	MONGODB_PASSWORD = "three_lane_Password_123" 
	SECRET_KEY = " three_lane_1899gwASdNs"
