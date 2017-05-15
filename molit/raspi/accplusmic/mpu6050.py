import smbus
import math
import time
import numpy
import threading
class MPU6050(threading.Thread):
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
		threading.Thread.__init__(self)
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

		self.gyro_calb_x=0		
		self.gyro_calb_y=0		
		self.gyro_calb_z=0		

		self.raw_temp=0
		self.scaled_temp=0

		self.accel_raw_x=0
		self.accel_raw_y=0
		self.accel_raw_z=0

		self.accel_scaled_x=0
		self.accel_scaled_y=0
		self.accel_scaled_z=0

		self.accel_calb_x=0		
		self.accel_calb_x=0		
		self.accel_calb_x=0		


		self.bus.write_byte_data(self.address, MPU6050.PWR_MGMT_1, 0)
		self.bus.write_byte_data(self.address, MPU6050.FS_SEL, self.fs_scale <<3 )
		self.bus.write_byte_data(self.address, MPU6050.AFS_SEL, self.afs_scale<<3)		

		self.th_a_xp=0
		self.th_a_xn=0
		self.th_a_yp=0
		self.th_a_yn=0
		self.th_a_zp=0
		self.th_a_zn=0

		self.th_g_xp=0
		self.th_g_xn=0
		self.th_g_yp=0
		self.th_g_yn=0
		self.th_g_zp=0
		self.th_g_zn=0

		self.msg="none"

	def read_data(self):
		#get_raw
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
		#calc_scale
		self.gyro_scaled_x=math.radians(self.gyro_raw_x / MPU6050.GYRO_SCALE[self.fs_scale][1])
		self.gyro_scaled_y=math.radians(self.gyro_raw_y / MPU6050.GYRO_SCALE[self.fs_scale][1])
		self.gyro_scaled_z=math.radians(self.gyro_raw_z / MPU6050.GYRO_SCALE[self.fs_scale][1])

		self.accel_scaled_x=self.accel_raw_x/MPU6050.ACCEL_SCALE[self.afs_scale][1]
		self.accel_scaled_y=self.accel_raw_y/MPU6050.ACCEL_SCALE[self.afs_scale][1]
		self.accel_scaled_z=self.accel_raw_z/MPU6050.ACCEL_SCALE[self.afs_scale][1]
		#calc_calb
		w1=[[0.976472616,-0.0155906985,-0.0124168191],[0.025918629,0.999177635,0.00923164655],[-0.00069146615,-0.00888237171,0.975103498]]
		b1=[0.00469431, 0.00632001, 0.11084614]
		b2=[0.0467816517944, -0.00318722237647, 0.00599268480517]
		acc_calb=numpy.dot([self.accel_scaled_x, self.accel_scaled_y, self.accel_scaled_z], w1) +b1
		gyro_calb=([self.gyro_scaled_x, self.gyro_scaled_y, self.gyro_scaled_z])+b2	
		
		self.accel_calb_x=acc_calb[0]	
		self.accel_calb_y=acc_calb[1]	
		self.accel_calb_z=acc_calb[2]
		self.gyro_calb_x=gyro_calb[0]
		self.gyro_calb_y=gyro_calb[1]
		self.gyro_calb_z=gyro_calb[2]
	
	def twos_complement(self, high,low):
		value=(high<<8)+low
		if(value>=0x8000):
			return -((0xffff-value)+1)
		else:
			return value
		print(high, low)
	def setting(self, count):
		self.read_data()
		self.th_g_xp=max(self.gyro_calb_x, self.th_g_xp)
		self.th_g_xn=min(self.gyro_calb_x, self.th_g_xn)
		self.th_g_yp=max(self.gyro_calb_y, self.th_g_yp)
		self.th_g_yn=min(self.gyro_calb_y, self.th_g_yn)
		self.th_g_zp=max(self.gyro_calb_z, self.th_g_zp)
		self.th_g_zn=min(self.gyro_calb_z, self.th_g_zn)

		self.th_a_xp=max(self.accel_calb_x, self.th_a_xp)	
		self.th_a_xn=min(self.accel_calb_x, self.th_a_xn)	
		self.th_a_yp=max(self.accel_calb_y, self.th_a_yp)	
		self.th_a_yn=min(self.accel_calb_y, self.th_a_yn)	
		self.th_a_zp=max(self.accel_calb_z, self.th_a_zp)	
		self.th_a_zn=min(self.accel_calb_z, self.th_a_zn)	
		if count%10==0:
			print("imu", count/10, "sec left")
			print('Acc')
			print(self.th_a_xp, self.th_a_xn)
			print(self.th_a_yp, self.th_a_yn)
			print(self.th_a_zp, self.th_a_zn)
			print('Gyro')
			print(self.th_g_xp, self.th_g_xn)
			print(self.th_g_yp, self.th_g_yn)
			print(self.th_g_zp, self.th_g_zn)
		count-=1
		timer=threading.Timer(0.1,self.setting,args=[count])
		if(count>0):
			timer.start()
		else:
			self.th_g_xp=1.5*self.th_g_xp
			self.th_g_xn=1.5*self.th_g_xn
			self.th_g_yp=1.5*self.th_g_yp
			self.th_g_yn=1.5*self.th_g_yn
			self.th_g_zp=1.5*self.th_g_zp
			self.th_g_zn=1.5*self.th_g_zn
	
			self.th_a_xp=1.5*self.th_a_xp	
			self.th_a_xn=1.5*self.th_a_xn	
			self.th_a_yp=1.5*self.th_a_yp	
			self.th_a_yn=1.5*self.th_a_yn	
			self.th_a_zp=1.5*self.th_a_zp	
			self.th_a_zn=1.5*self.th_a_zn	
		
	def run(self):
		while True:
			self.read_data()
			if not(self.th_a_xn<self.accel_calb_x<self.th_a_xp):
				self.msg="Shaking!"
			if not(self.th_a_yn<self.accel_calb_y<self.th_a_yp):
				self.msg="Shaking!"
			if not(self.th_a_zn<self.accel_calb_z<self.th_a_zp):
				self.msg="Shaking!"
			if not(self.th_g_xn<self.gyro_calb_x<self.th_g_xp):
				self.msg="Shaking!"
			if not(self.th_g_yn<self.gyro_calb_y<self.th_g_yp):
				self.msg="Shaking!"
			if not(self.th_g_zn<self.gyro_calb_z<self.th_g_zp):
				self.msg="Shaking!"
			time.sleep(0.1)
		#	timer=threading.Timer(time,self.exam,args=[time])
		#	timer.start()

#/////////////////////////////////////////////////////////////
if __name__=='__main__':
	sensor1=MPU6050(smbus.SMBus(1), 0x68, MPU6050.FS_500, MPU6050.AFS_4g)#bus/addr
#	sensor1.setting(50)
	while True:
#		print(sensor1.exam())
		sensor1.read_data()
		print(sensor1.accel_calb_x)
		time.sleep(0.005)
