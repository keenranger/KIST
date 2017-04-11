import numpy as np
import tensorflow as tf

xy = np.loadtxt('asd.txt', unpack=True)

x1_data = np.transpose( xy[0:1])
y1_data = np.transpose( xy[3:4])
x2_data = np.transpose( xy[1:2])
y2_data = np.transpose( xy[4:5])
x3_data = np.transpose( xy[2:3])
y3_data = np.transpose( xy[5:6])



W = tf.Variable([1.], tf.float32)
b = tf.Variable([-.3], tf.float32)


X = tf.placeholder(tf.float32)
Y = tf.placeholder(tf.float32)

linear_model = W*X+b

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
    # Run graph.
    for step in range(10001):
        sess.run(train, feed_dict={X:x1_data, Y:y1_data})
        if step % 1000 == 0:
             print (step, sess.run(W), sess.run(b))
             
             
    sess.run(init)
    # Run graph.
    for step in range(10001):
        sess.run(train, feed_dict={X:x2_data, Y:y2_data})
        if step % 1000 == 0:
             print (step, sess.run(W), sess.run(b))
             
             
    sess.run(init)
    # Run graph.
    for step in range(10001):
        sess.run(train, feed_dict={X:x3_data, Y:y3_data})
        if step % 1000 == 0:
             print (step, sess.run(W), sess.run(b))

            