import spidev

import time

from firebase import firebase

from pyrebase import pyrebase

spi = spidev.SpiDev()

spi.open(0,0)

spi.max_speed_hz = 1350000

 

config = {

    "apiKey" : "AIzaSyDBfEBZUOPjEP6wZBwtG7zC5hENqFPP9NE",

    "authDomain" : "gamzi-655a1.firebaseapp.com",

    "databaseURL" : "https://gamzi-655a1-default-rtdb.firebaseio.com",

    "projectId" : "gamzi-655a1",

    "storageBucket" : "gamzi-655a1.appspot.com",

    "messagingSenderId" : "273237078698",

    "appId" : "1:273237078698:web:60d0608b864b65b867d6d3"

}

 

firebase = pyrebase.initialize_app(config)

 

db = firebase.database()

 

def analog_read(channel):

	r = spi.xfer2([1, (8 + channel) <<4, 0])

	adc_out = ((r[1]&3) << 8) + r[2]

	return adc_out

 

while True:

	reading = analog_read(0)

	voltage = reading * 5.0/ 1024 

	Rs_gas =(5.0-voltage)/voltage

	R0 = 105789.47368421052

	ratio = Rs_gas/R0

	x=1538.46 * ratio

	value = pow(x,-1.709)

	ppm = round(value)

	print(ppm)

	db.child("sensorList").child("sensorId").update({"id":"ad3d8fj9","ppm":ppm,})

	time.sleep(5)
