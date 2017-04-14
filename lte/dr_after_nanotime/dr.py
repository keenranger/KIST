import numpy as np
# import tensorflow as tf
import matplotlib.pyplot as plt
from matplotlib import animation
import math

sen_data = np.loadtxt('sen1.txt', unpack=True)
car_data = np.loadtxt('car1.txt', unpack=True)

sen = np.transpose(sen_data)
car = np.transpose(car_data)

# heading start
time = 0.0
deg = 0.
flag = 0
for row in sen:
    if flag == 0:
        time = row[0]
        array_g = np.array([[time, 0]])#as we have flag, make array in if statement
        flag = 1
        continue
    deg += row[6] * (row[0] - time) * pow(10, -9)#row[6]is rad per sec, and time is ns, so multiply 10^-9
    array_g = np.concatenate(
        (array_g, (np.array([[row[0], math.degrees(deg)]]))), axis=0)
    time = row[0]
# heading end
# peak start
array_y = np.array([[0, 0]])#no flag, make array in advance
thres = 0.
flag = 0
time = 0.
for row in car:
    if flag == 0:#finding high peak
        if row[2] > thres:#find biggest value and refresh time
            thres = row[2]
            time = row[0]
        if row[0] - time > pow(10, 8):#check whether it`s time interval between last low peak over 0.1s
            if row[2] < 0 and thres > 12000:#if value become lower than 0 and saved thres value is enough
                array_y = np.concatenate(
                    (array_y, (np.array([[time, thres]]))), axis=0)
                thres = 0.
                flag = 1
    if flag == 1:#finding low peak
        if row[2] < thres:#find smallest value and refresh time
            thres = row[2]
            time = row[0]
        if row[0] - time > pow(10, 8):#check whether it`s time interval between last low peak over 0.1s
            if row[2] > 0 and thres < -12000:#if value become bigger than 0 and saved thres value is enough
                array_y = np.concatenate(
                    (array_y, (np.array([[time, thres]]))), axis=0)
                thres = 0.
                flag = 0
array_y = array_y[1:, :]#remove first line
# peak end

# vel start
array_v = np.array([[0, 0]])#make array in advance
time = 0.
for row in array_y:
    if time != 0:#compute since second component come
        array_v = np.concatenate(
            (array_v, (np.array([[time, (2.0960 / 2.) / ((row[0] - time) * pow(10, -9))]]))), axis=0)
            #2.0960 is circumference of wheel, and since we can detect peaks that let us know time interval during half rev
            #divide it two. wheel length is meter, row minus time is ns, so multiply 10^-9
    time = row[0]
array_v = array_v[1:, :]
# vel end

# print(array_v)


# dr start
time = 0.
inv = 0.
a = 0
temp=0.
for row in array_g:
    if time == 0:
        array_d = np.array([[row[0], 0, 0]])#first row, save init time
        time = row[0]
        continue
    inv = (row[0] - time)#time interval between array_g row : ns
    time = row[0]
    dist = 0.
    if row[0]<array_v[0,0] or row[0]>array_v[-1,0]:#if gyro data is out of range of velocity data, don`t check it
        continue
    for row2 in array_v:#to sync time between velocity and heading. check vel for every heading.
        vel=row2[1]
#            dist = inv * pow(10, -9) * row2[1]#inv is nano second, row2[1] array_v is m/s so multiply 10^-9
        if row[0] < row2[0]:
            dist = inv * pow(10, -9) * vel#inv is nano second, row2[1] array_v is m/s so multiply 10^-9
            temp+=dist
            break
    array_d = np.concatenate(
        (array_d, (np.array([[(inv), dist * math.cos(math.radians(row[1])), dist * math.sin(math.radians(row[1]))]]))), axis=0)#first row: init time and 0,0 other row: time past after last row and distance during that period
# dr end
array_dr = np.cumsum(array_d, axis=0)#1st row : init time and 0,0  other row : time and x,y
# print(array_d[:,1])
plt.plot(array_dr[:, 1],array_dr[:, 2])
# plt.plot(array_v[:,0],array_v[:,1])
print(temp)
# plt.plot(array_dr[:,1],array_dr[:,2])
# plt.savefig('temp.png')
# print(array_d[:,0])
plt.show()

# fig,ax= plt.subplots()
# xdata, ydata = [], []
# ln, = plt.plot([], [], 'ro', lw=3)
#
# def init():
#     # ax.set_xlim(-50, 50)
#     # ax.set_ylim(-50, 50)
#     ln.set_data([], [])
#     ax.plot(array_dr[:,1],array_dr[:,2])
#     return ln,
#
# def animate(i):
#     # xdata.append(array_dr[i*10,1])
#     # ydata.append(array_dr[i*10,2])
#     # ln.set_data(xdata, ydata)
#     ln.set_data(array_dr[i*10,1],array_dr[i*10,2])
#
#     return ln,
#
#
# ani = animation.FuncAnimation(fig, animate, interval=0.0001,
#                     init_func=init, blit=False)
# ani.save('bicycle.mp4',fps =15)
# plt.show()
