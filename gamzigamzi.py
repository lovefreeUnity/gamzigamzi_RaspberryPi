import spidev
import time
from firebase import firebase

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1350000

firebase= firebase.FirebaseApplication('https://gamzi-655a1-default-rtdb.firebaseio.com/',None)

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
	firebase.put("Raspberrypi2","name","raspbrrypi2")
	firebase.put("Raspberrypi2","ppm",ppm)
	time.sleep(5)