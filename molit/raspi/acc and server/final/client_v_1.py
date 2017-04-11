import socket
import sys
import smbus
import time
import mpu6050



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
	ID='AAA'
	#connect
	HOST = '192.168.0.200'
	PORT = int(sys.argv[1])
	print ('Client :: Conncet to ', HOST, PORT)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	print('connected')
	msg=ID+'attached'
	s.send(msg.encode(encoding='utf_8', errors='strict'))
	#sensor_setting
	sensor1=mpu6050.MPU6050(smbus.SMBus(1), 0x68, mpu6050.MPU6050.FS_500, mpu6050.MPU6050.AFS_4g)#bus/addr
	sensor1.setting(100)
	#data = s.recv(1024)
	#print ('Client :: recv : ', data.decode())
	while True:
		msg=sensor1.exam()
		if msg=='Alert!!!!!!':
			msg=ID+msg
			print(msg)	
			s.send(msg.encode(encoding='utf_8', errors='strict'))
		time.sleep(0.3)
