# -*- coding: utf-8 -*-

import numpy as np
import tensorflow as tf

def xavier_init(n_inputs, n_outputs, uniform = True):
    if uniform:
        init_range = tf.sqrt(6.0/ (n_inputs + n_outputs))
        return tf.random_uniform_initializer(-init_range, init_range)

    else:
        stddev = tf.sqrt(3.0 / (n_inputs + n_outputs))
        return tf.truncated_normal_initializer(stddev=stddev)

xy = np.loadtxt('asd.txt', unpack=True)

x_data = np.transpose( xy[0:3])
y_data = np.transpose( xy[3:6])

#W1 = tf.Variable(tf.random_uniform([3, 3], -.0, 1.0))
#W2 = tf.Variable(tf.random_uniform([3, 3], -.0, 1.0))
#W3 = tf.Variable(tf.random_uniform([3, 3], -.0, 1.0)) 
#W1 = tf.get_variable("W1", shape=[3,3], initializer=xavier_init(3,3))
W2 = tf.get_variable("W2", shape=[3,3], initializer=xavier_init(3,3))
#b1 = tf.Variable(tf.zeros([3]))
b2 = tf.Variable(tf.zeros([3]))


X = tf.placeholder(tf.float32, [None, 3])
Y = tf.placeholder(tf.float32, [None, 3])


#linear_model1 =tf.nn.sigmoid(tf.matmul(X,W1)+b1)
linear_model2 =tf.matmul(X,W2)+b2

# Cost function 
cost = tf.reduce_mean(tf.reduce_sum(tf.square(linear_model2-Y)))


# Minimize cost.
a = tf.Variable(0.001)
optimizer = tf.train.AdamOptimizer(a)
train = optimizer.minimize(cost)

# Initializa all variables.
init = tf.initialize_all_variables()


# Launch the graph
with tf.Session() as sess:
    
    sess.run(init)
    # Run graph.
    for step in range(50001):
        sess.run(train, feed_dict={X:x_data, Y:y_data})
        if step % 5000 == 0:
             print (step)
#             print (sess.run(W1))
 #            print (sess.run(b1))
             print (sess.run(W2))
             print (sess.run(b2))
             print (sess.run(cost, feed_dict={X:x_data, Y:y_data}))
             
             

            