# -*- coding: utf-8 -*-

import numpy as np
import tensorflow as tf

xy = np.loadtxt('asd.txt', unpack=True)

x_data = np.transpose( xy[0:3])
y_data = np.transpose( xy[3:6])


W = tf.Variable(tf.random_uniform([3, 3], 0.9, 1.0))
b = tf.Variable(tf.zeros([3]))


X = tf.placeholder(tf.float32, [None, 3])
Y = tf.placeholder(tf.float32, [None, 3])

linear_model =tf.matmul(X,W)+b

# Cost function 
cost = tf.reduce_mean(tf.reduce_sum(tf.square(linear_model-Y)))


# Minimize cost.
a = tf.Variable(0.001)
optimizer = tf.train.AdamOptimizer(a)
train = optimizer.minimize(cost)

# Initializa all variables.
init = tf.initialize_all_variables()


# Launch the graph
with tf.Session() as sess:
    
    sess.run(init)
    print(sess.run(linear_model, feed_dict={X:x_data}))
    # Run graph.
    for step in range(10001):
        sess.run(train, feed_dict={X:x_data, Y:y_data})
        if step % 1000 == 0:
             print (step)
             print (sess.run(W))
             print (sess.run(b))
             print (sess.run(cost, feed_dict={X:x_data, Y:y_data}))
             
             

            