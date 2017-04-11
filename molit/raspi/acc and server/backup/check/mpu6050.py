import smbus
import math
import time

class MPU6050(object):
	PWR_MGMT_1=0x6b
	FS_SEL=0x1b
	FS_250=0
	FS_500=1
	FS_1000=2
	FS_2000=3
	
	AFS_SEL=0x1c
	AFS_2g=0
	AFS_4g=1
	AFS_8g=2
	AFS_16g=3

	ACCEL_START_BLOCK=0x3b
	ACCEL_XOUT_H=0
	ACCEL_XOUT_L=1
	ACCEL_YOUT_H=2
	ACCEL_YOUT_L=3
	ACCEL_ZOUT_H=4
	ACCEL_ZOUT_L=5
	ACCEL_SCALE={AFS_2g:[2, 16384.0],AFS_4g:[4, 8192.0], AFS_8g:[8,4096.0], AFS_16g:[16, 2048.0]}

	TEMP_START_BLOCK=0X41
	TEMP_OUT_H=0
	TEMP_OUT_L=1

	GYRO_START_BLOCK=0X43
	GYRO_XOUT_H=0
	GYRO_XOUT_L=1
	GYRO_YOUT_H=2
	GYRO_YOUT_L=3
	GYRO_ZOUT_H=4
	GYRO_ZOUT_L=5
	GYRO_SCALE={FS_250:[250, 131.0], FS_500:[500,65.5], FS_1000:[1000, 32.8], FS_2000:[2000,16.4]}

	def __init__(self, bus, address, fs_scale, afs_scale):
		self.bus=bus
		self.address=address
		self.fs_scale=fs_scale
		self.afs_scale=afs_scale

		self.raw_gyro_data=[0, 0, 0, 0, 0, 0]
		self.raw_accel_data=[0, 0, 0, 0, 0, 0]
		self.raw_temp_data=[0, 0]

		self.gyro_raw_x=0
		self.gyro_raw_y=0
		self.gyro_raw_z=0

		self.gyro_scaled_x=0
		self.gyro_scaled_y=0
		self.gyro_scaled_z=0

		self.raw_temp=0
		self.scaled_temp=0

		self.accel_raw_x=0
		self.accel_raw_y=0
		self.accel_raw_z=0

		self.accel_scaled_x=0
		self.accel_scaled_y=0
		self.accel_scaled_z=0

		self.bus.write_byte_data(self.address, MPU6050.PWR_MGMT_1, 0)
		self.bus.write_byte_data(self.address, MPU6050.FS_SEL, self.fs_scale <<3 )
		self.bus.write_byte_data(self.address, MPU6050.AFS_SEL, self.afs_scale<<3)		
	def read_raw_data(self):
		self.raw_gyro_data=self.bus.read_i2c_block_data(self.address, MPU6050.GYRO_START_BLOCK, 6)
		self.raw_accel_data=self.bus.read_i2c_block_data(self.address, MPU6050.ACCEL_START_BLOCK, 6)
		self.raw_temp_data=self.bus.read_i2c_block_data(self.address, MPU6050.TEMP_START_BLOCK, 2)
		self.gyro_raw_x=self.twos_complement(self.raw_gyro_data[MPU6050.GYRO_XOUT_H], self.raw_gyro_data[MPU6050.GYRO_XOUT_L])
		self.gyro_raw_y=self.twos_complement(self.raw_gyro_data[MPU6050.GYRO_YOUT_H], self.raw_gyro_data[MPU6050.GYRO_YOUT_L])
		self.gyro_raw_z=self.twos_complement(self.raw_gyro_data[MPU6050.GYRO_ZOUT_H], self.raw_gyro_data[MPU6050.GYRO_ZOUT_L])

		self.accel_raw_x=self.twos_complement(self.raw_accel_data[MPU6050.ACCEL_XOUT_H], self.raw_accel_data[MPU6050.ACCEL_XOUT_L])
		self.accel_raw_y=self.twos_complement(self.raw_accel_data[MPU6050.ACCEL_YOUT_H], self.raw_accel_data[MPU6050.ACCEL_YOUT_L])
		self.accel_raw_z=self.twos_complement(self.raw_accel_data[MPU6050.ACCEL_ZOUT_H], self.raw_accel_data[MPU6050.ACCEL_ZOUT_L])

		self.raw_temp=self.twos_complement(self.raw_temp_data[MPU6050.TEMP_OUT_H], self.raw_temp_data[MPU6050.TEMP_OUT_L])

		self.gyro_scaled_x=math.radians(self.gyro_raw_x / MPU6050.GYRO_SCALE[self.fs_scale][1])
		self.gyro_scaled_y=math.radians(self.gyro_raw_y / MPU6050.GYRO_SCALE[self.fs_scale][1])
		self.gyro_scaled_z=math.radians(self.gyro_raw_z / MPU6050.GYRO_SCALE[self.fs_scale][1])

		self.accel_scaled_x=self.accel_raw_x/MPU6050.ACCEL_SCALE[self.afs_scale][1]
		self.accel_scaled_y=self.accel_raw_y/MPU6050.ACCEL_SCALE[self.afs_scale][1]
		self.accel_scaled_z=self.accel_raw_z/MPU6050.ACCEL_SCALE[self.afs_scale][1]

	def read_scaled_gyro_x(self):
		return self.gyro_scaled_x
	def read_scaled_gyro_y(self):
		return self.gyro_scaled_y
	def read_scaled_gyro_z(self):
		return self.gyro_scaled_z
	def read_scaled_accel_x(self):
		return self.accel_scaled_x
	def read_scaled_accel_y(self):
		return self.accel_scaled_y
	def read_scaled_accel_z(self):
		return self.accel_scaled_z
	def read_temp(self):
		return self.scaled_temp

	def twos_complement(self, high,low):
		value=(high<<8)+low
		if(value>=0x8000):
			return -((0xffff-value)+1)
		else:
			return value
		print(high, low)

sensor1=MPU6050(smbus.SMBus(1), 0x68, MPU6050.FS_500, MPU6050.AFS_4g)#bus/addr

th_a_xp=0.
th_a_xn=0.
th_a_yp=0.
th_a_yn=0.
th_a_zp=0.
th_a_zn=0.

th_g_xp=0.
th_g_xn=0.
th_g_yp=0.
th_g_yn=0.
th_g_zp=0.
th_g_zn=0.

#with open("data.txt", 'w')as output:
for i in range(100):
	sensor1.read_raw_data()
	gyro_xout = sensor1.read_scaled_gyro_x()
	gyro_yout = sensor1.read_scaled_gyro_y()
	gyro_zout = sensor1.read_scaled_gyro_z()
	accel_xout = sensor1.read_scaled_accel_x()
	accel_yout = sensor1.read_scaled_accel_y()
	accel_zout = sensor1.read_scaled_accel_z()
	time.sleep(0.1)
	th_a_xp=max(accel_xout, th_a_xp)
	th_a_xn=min(accel_xout, th_a_xn)
	th_a_yp=max(accel_yout, th_a_yp)
	th_a_yn=min(accel_yout, th_a_yn)
	th_a_zp=max(accel_zout, th_a_zp)
	th_a_zn=min(accel_zout, th_a_zn)

	th_g_xp=max(gyro_xout, th_g_xp)
	th_g_xn=min(gyro_xout, th_g_xn)
	th_g_yp=max(gyro_yout, th_g_yp)
	th_g_yn=min(gyro_yout, th_g_yn)
	th_g_zp=max(gyro_zout, th_g_zp)
	th_g_zn=min(gyro_zout, th_g_zn)

	
	if i%10==0:
		print(i/10, "sec")
		print('Acc')
		print(th_a_xp, th_a_xn)
		print(th_a_yp, th_a_yn)
		print(th_a_zp, th_a_zn)
		print('Gyro')
		print(th_g_xp, th_g_xn)
		print(th_g_yp, th_g_yn)
		print(th_g_zp, th_g_zn)

while True:
	flag=0
	sensor1.read_raw_data()
	gyro_xout = sensor1.read_scaled_gyro_x()
	gyro_yout = sensor1.read_scaled_gyro_y()
	gyro_zout = sensor1.read_scaled_gyro_z()
	accel_xout = sensor1.read_scaled_accel_x()
	accel_yout = sensor1.read_scaled_accel_y()
	accel_zout = sensor1.read_scaled_accel_z()
	if not(th_a_xn<accel_xout and accel_xout<th_a_xp):
		flag=1
	if not(th_a_yn<accel_yout and accel_yout<th_a_yp):
		flag=1
	if not(th_a_zn<accel_zout and accel_zout<th_a_zp):
		flag=1

	if not(th_g_xn<gyro_xout and gyro_xout<th_g_xp):
		flag=1
	if not(th_g_yn<gyro_yout and gyro_yout<th_g_yp):
		flag=1
	if not(th_g_zn<gyro_zout and gyro_zout<th_g_zp):
		flag=1
	if flag==1:
		print("Alert!!!!!!")
	else:
		print("I`m fine")
	time.sleep(0.1)

