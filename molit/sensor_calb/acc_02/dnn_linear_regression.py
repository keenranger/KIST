import numpy as np
import tensorflow as tf

xy = np.loadtxt('traindatatrue.txt', unpack=True)

x_data = np.transpose( xy[0:3])
x_square=np.power(x_data,2)
x_tri=np.power(x_data,3)
y_data = np.transpose( xy[3:6])


W1 = tf.Variable(tf.random_uniform([3, 3], 0.9, 1.0))
W2 = tf.Variable(tf.random_uniform([3, 3], 0.9, 1.0))
W3 = tf.Variable(tf.random_uniform([3, 3], 0.9, 1.0))
b = tf.Variable(tf.zeros([3]))


X1 = tf.placeholder(tf.float32, [None, 3])
X2 = tf.placeholder(tf.float32, [None, 3])
X3 = tf.placeholder(tf.float32, [None, 3])
Y = tf.placeholder(tf.float32, [None, 3])

linear_model =tf.matmul(X1,W1)+tf.matmul(X2,W2)+tf.matmul(X3,W3)+b

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
    for step in range(50001):
        sess.run(train, feed_dict={X1:x_tri, X2:x_square, X3:x_data, Y:y_data})
        if step % 5000 == 0:
             print (step)
             print (sess.run(W1))
             print (sess.run(W2))
             print (sess.run(W3))
             print (sess.run(b))
             print (sess.run(cost, feed_dict={X1:x_tri, X2:x_square, X3:x_data, Y:y_data}))
             
             

            