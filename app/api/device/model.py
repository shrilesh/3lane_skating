from app import db
from flask_mongokit import Document
from bson import ObjectId 

class Device(Document):
	__collection__= "device"
	structure = {
		"status": str,
		"lane_no": str,
		"start": str,
		"final": str,
		"result":int,
		"extra":dict
		}
	required_fields = ["lane_no"]
	default_values = {'extra':{}}

	# def addDeviceDetails(self, device_data):
	# 	db.device.insert(device_data)
	# 	return True

	def addDeviceData(self, device_data):
		print "Inside model addDeviceData"
		try:
			device_id = db.device.insert(device_data)
			return {
					"status": True,
					"device_id": device_id,
					"message": "Device data added sucessfully"
				}

		except Exception, e:
			return {
				"status": False,
				"message": "Device addition failed %s" %e
			}

	# def getData(self, device):
	#  	db.device.find(device)
	# 	return device

	 
	
		

db.register([Device])