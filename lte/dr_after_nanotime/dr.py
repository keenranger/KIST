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
array_g = np.array([[0, 0]])
for row in sen:
    if flag == 0:
        time = row[0]
        flag = 1
        continue
    deg += row[6] * (row[0] - time) * pow(10, -9)
    array_g = np.concatenate(
        (array_g, (np.array([[row[0], math.degrees(deg)]]))), axis=0)
    time = row[0]
array_g = array_g[1:, :]
# heading end

# plt.plot(sen[:,0],sen[:,6])

# peak start
array_y = np.array([[0, 0]])
thres = 0.
flag = 0
time = 0.
for row in car:
    if flag == 0:
        if time == 0. or row[0] - time > pow(10, 8):
            if row[2] > thres:
                thres = row[2]
                time = row[0]
            if row[2] < 0 and thres > 12000:
                array_y = np.concatenate(
                    (array_y, (np.array([[time, thres]]))), axis=0)
                thres = 0.
                flag = 1
    if flag == 1:
        if row[0] - time > pow(10, 8):
            if row[2] < thres:
                thres = row[2]
                time = row[0]
            if row[2] > 0 and thres < -12000:
                array_y = np.concatenate(
                    (array_y, (np.array([[time, thres]]))), axis=0)
                thres = 0.
                flag = 0
array_y = array_y[1:, :]
# peak end

# vel start
array_v = np.array([[0, 0]])
time = 0.
for row in array_y:
    if time != 0:
        array_v = np.concatenate(
            (array_v, (np.array([[time, (2.0960 / 2.) / ((row[0] - time) * pow(10, -9))]]))), axis=0)
    time = row[0]
array_v = array_v[1:, :]
# vel end

# dr start
time = 0.
inv = 0.
a = 0
for row in array_g:
    a += 1
    if time == 0:
        array_d = np.array([[row[0], 0, 0]])
        time = row[0]
    inv = (row[0] - time)*pow(10,-9)
    time = row[0]
    dist = 0.
    for row2 in array_v:
        if row[0] > row2[0]:
            dist = inv * row2[1]
            break
    array_d = np.concatenate(
        (array_d, (np.array([[(inv), dist * math.cos(math.radians(row[1])), dist * math.sin(math.radians(row[1]))]]))), axis=0)
# dr end
array_dr=np.cumsum(array_d,axis=0)

plt.plot(array_dr[:,1],array_dr[:,2])
# plt.savefig('temp.png')
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

# print(np.cumsum(array_d,axis=0))

# plt.plot(np.cumsum(array_d, axis=0)[:, 1], np.cumsum(array_d, axis=0)[:, 2],hold=False)
# plt.show()

    # plt.plot(row[1],row[2],'r+')

# plt.hold(False)
# plt.plot(1,1,'r+')
# plt.show()
# plt.plot(sen[:,0],sen[:,5])

# print(array_d)
# plt.plot(array_v[:, 0], array_v[:, 1])
# plt.plot(array_y[:,0], array_y[:,1])
# plt.show()

# plt.subplot(3, 2, 1)
# plt.plot(sen[:, 1])
# plt.subplot(3, 2, 2)
# plt.plot(sen[:, 2])
# plt.subplot(3, 2, 3)
# plt.plot(sen[:, 3])
# plt.subplot(3, 2, 4)
# plt.plot(sen[:, 4])
# plt.subplot(3, 2, 5)
# plt.plot(sen[:, 5])
# plt.subplot(3, 2, 6)
# plt.plot(sen[:, 6])

# W = tf.Variable(tf.random_uniform([3, 3], 0.9, 1.0))
# b = tf.Variable(tf.zeros([3]))
#
#
# X = tf.placeholder(tf.float32, [None, 3])
# Y = tf.placeholder(tf.float32, [None, 3])
#
# linear_model = tf.matmul(X, W) + b
#
# # Cost function
# cost = tf.reduce_sum(tf.square(linear_model - Y))
#
#
# # Minimize cost.
# a = tf.Variable(0.001)
# optimizer = tf.train.AdamOptimizer(a)
# train = optimizer.minimize(cost)
#
# # Initializa all variables.
# init = tf.initialize_all_variables()
# train_cost = []
# test_cost = []
# # Launch the graph
# with tf.Session() as sess:
#     sess.run(init)
#     # Run graph.
#     for step in range(1001):
#         sess.run(train, feed_dict={X: train_acc, Y: train_true})
#         if step < 2000:
#             train_cost.append(
#                 sess.run(cost, feed_dict={X: train_acc, Y: train_true}) / 7)
#             test_cost.append(
#                 sess.run(cost, feed_dict={X: test_acc, Y: test_true}) / 3)
#         if step % 1000 == 0:
#             print(step)
#             print(sess.run(W))
#             print(sess.run(b))
#             print(sess.run(cost, feed_dict={X: train_acc, Y: train_true}))
#     print("-" * 20)
#     print("train cost:", sess.run(
#         cost, feed_dict={X: train_acc, Y: train_true}) / 7)
#     print("true  cost:", sess.run(
#         cost, feed_dict={X: test_acc, Y: test_true}) / 3)
#     print(np.mean(data[:, 4]), np.mean(data[:, 5]), np.mean(data[:, 6]))
#     plt.subplot(2, 2, 1)
#     plt.title('Cost')
#     plt.plot(train_cost, 'b-', label='train')
#     plt.plot(test_cost, 'r-', label='test')
#     plt.legend(loc='upper right')
#     plt.grid('k', linestyle='-', linewidth=0.1)
#
#     plt.subplot(2, 2, 2)
#     plt.title('X(Test Data)')
#     plt.plot(test_acc[:, 0], 'b-', label='Raw')
#     plt.plot(sess.run(linear_model[:, 0], feed_dict={X: test_acc, Y: test_true}), 'r-', label='Calb')
#     plt.legend(loc='upper right')
#     plt.grid('k', linestyle='-', linewidth=0.1)
#
#     plt.subplot(2, 2, 3)
#     plt.title('Y(Test Data)')
#     plt.plot(test_acc[:, 1], 'b-', label='Raw')
#     plt.plot(sess.run(linear_model[:, 1], feed_dict={X: test_acc, Y: test_true}), 'r-', label='Calb')
#     plt.legend(loc='upper right')
#     plt.grid('k', linestyle='-', linewidth=0.1)
#
#     plt.subplot(2, 2, 4)
#     plt.title('Z(Test Data)')
#     plt.plot(test_acc[:, 2], 'b-', label='Raw')
#     plt.plot(sess.run(linear_model[:, 2], feed_dict={
#              X: test_acc, Y: test_true}), 'r-', label='Calb')
#     plt.legend(loc='upper right')
#     plt.grid('k', linestyle='-', linewidth=0.1)
#     plt.show()
