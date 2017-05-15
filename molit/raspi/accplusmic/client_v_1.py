import socket
import sys
import smbus
import time
import mpu6050
import SWHear


def isNumber(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

if __name__=="__main__":
	if len(sys.argv) == 1:
		print('usage: python tcpClient.py port_number')
		exit(1)
	elif not isNumber(sys.argv[1]):
		print ('Invalid port_number, ', sys.argv[1])
		exit(2)
	ID='[AAA]'
	#connect
	HOST = '192.168.0.200'
	PORT = int(sys.argv[1])
	print ('Client :: Conncet to ', HOST, PORT)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	print('connected')
	msg=ID+'attached\n'
	s.send(msg.encode(encoding='utf_8', errors='strict'))

	#sensor_setting
	sensor1=mpu6050.MPU6050(smbus.SMBus(1), 0x68, mpu6050.MPU6050.FS_500, mpu6050.MPU6050.AFS_4g)#bus/addr
	mic1=SWHear.SWHear(updatesPerSecond=5)
	mic1.stream_start()
	sensor1.setting(100)
	mic1.setting(50)
	time.sleep(12)
	sensor1.start()
	mic1.start()
	while True:
		if sensor1.msg=='Shaking!':
			msg=ID+sensor1.msg+"\n"
			sensor1.msg="none"
			print(msg)	
			s.send(msg.encode(encoding='utf_8', errors='strict'))
		if mic1.msg=='Noise!':
			msg=ID+mic1.msg+']'+str(mic1.value)+"\n"
			mic1.msg="none"
			mic1.value=0
			print(msg)	
			s.send(msg.encode(encoding='utf_8', errors='strict'))
