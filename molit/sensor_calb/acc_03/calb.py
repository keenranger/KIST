import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

data_raw = np.loadtxt('data.txt', unpack=True)
true_raw = np.loadtxt('true.txt', unpack=True)

print(data_raw)
data = np.transpose( data_raw[0:7])
true = np.transpose( true_raw[0:3])

train_data=np.concatenate((data[0:7000],data[10200:17200],data[20400:27400],data[30600:37600],data[41200:48200]), axis=0)
test_data=np.concatenate((data[7000:10000],data[17200:20200],data[27400:30400],data[37600:40600],data[48200:51200]),axis=0)

train_true=np.concatenate((true[0:7000],true[10000:17000],true[20000:27000],true[30000:37000],true[40000:47000]), axis=0)
test_true=np.concatenate((true[7000:10000],true[17000:20000],true[27000:30000],true[37000:40000],true[47000:50000]),axis=0)

train_acc=train_data[:,1:4]
test_acc=test_data[:,1:4]

W = tf.Variable(tf.random_uniform([3, 3], 0.9, 1.0))
b = tf.Variable(tf.zeros([3]))


X = tf.placeholder(tf.float32, [None, 3])
Y = tf.placeholder(tf.float32, [None, 3])


linear_model =tf.matmul(X,W)+b

# Cost function 
cost = tf.reduce_sum(tf.square(linear_model-Y))


# Minimize cost.
a = tf.Variable(0.001)
optimizer = tf.train.AdamOptimizer(a)
train = optimizer.minimize(cost)

# Initializa all variables.
init = tf.initialize_all_variables()
train_cost=[]
test_cost=[]
# Launch the graph
with tf.Session() as sess:
    sess.run(init)
    # Run graph.
    for step in range(5001):
        sess.run(train, feed_dict={X:train_acc, Y:train_true})
        if step <2000:
            train_cost.append(sess.run(cost, feed_dict={X:train_acc, Y:train_true})/7)
            test_cost.append(sess.run(cost, feed_dict={X:test_acc, Y:test_true})/3)
        if step % 1000==0:
             print (step)
             print (sess.run(W))
             print (sess.run(b))
             print (sess.run(cost, feed_dict={X:train_acc, Y:train_true}))
    print("-"*20)
    print("train cost:",sess.run(cost, feed_dict={X:train_acc, Y:train_true})/7)
    print("true  cost:",sess.run(cost, feed_dict={X:test_acc, Y:test_true})/3)
    print(np.mean(data[:,4]), np.mean(data[:,5]), np.mean(data[:,6]))

    plt.subplot(2,2,1)
    plt.title('Cost')
    plt.plot(train_cost, 'b-', label='train')
    plt.plot(test_cost, 'r-', label='test')
    plt.legend(loc='upper right')
    plt.grid('k', linestyle='-', linewidth=0.1)
    
    plt.subplot(2,2,2)
    plt.title('X(Test Data)')
    plt.plot(test_acc[:,0], 'b-', label='Raw')
    plt.plot(sess.run(linear_model[:,0], feed_dict={X:test_acc, Y:test_true}), 'r-', label='Calb')
    plt.legend(loc='upper right')
    plt.grid('k', linestyle='-', linewidth=0.1)
    
    plt.subplot(2,2,3)
    plt.title('Y(Test Data)')
    plt.plot(test_acc[:,1], 'b-', label='Raw')
    plt.plot(sess.run(linear_model[:,1], feed_dict={X:test_acc, Y:test_true}), 'r-', label='Calb')
    plt.legend(loc='upper right')
    plt.grid('k', linestyle='-', linewidth=0.1)
    
    plt.subplot(2,2,4)
    plt.title('Z(Test Data)')
    plt.plot(test_acc[:,2], 'b-', label='Raw')
    plt.plot(sess.run(linear_model[:,2], feed_dict={X:test_acc, Y:test_true}), 'r-', label='Calb')   
    plt.legend(loc='upper right')
    plt.grid('k', linestyle='-', linewidth=0.1)
    
    plt.show
                 
             

            