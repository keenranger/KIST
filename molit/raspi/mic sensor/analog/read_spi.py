import spidev
import time

spi=spidev.SpiDev()
spi.open(0,0)

def analog_read(channel):
	r=spi.xfer2([1,(8+channel)<<4,0])
	adc_out=((r[1]&3)<<8)+r[2]
	return adc_out

with open('micdata.txt', 'w') as output:
	for i in range(1000):
		temp=analog_read(0)
#		print(temp,file=output)
		print(temp)
		time.sleep(0.01)
