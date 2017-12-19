import tensorflow as tf
import numpy as np
import time
#from tensorflow.examples.tutorials.mnist import input_data

class TFNN:
    def __init__(self, dimensions, weights = None):
        #dimensions = [tf.constant(dim, dtype=tf.int32) for dim in dimensions]
        self.input_size = dimensions[0]
        self.output_size = dimensions[-1]
        self.dimensions = list(zip(dimensions[:-1], dimensions[1:]))
        self.weights = [self.init_weights(dim) for dim in self.dimensions]

        self.init_session()

    def init_weights(self, shape):
        return tf.Variable(tf.random_normal(shape, stddev=0.01)).initialized_value()

    def init_session(self):
        self.sess = tf.Session()

    def model(self, X, weights):
        h = X
        for w in weights[:-1]:
            h = tf.nn.relu(tf.matmul(h, w))

        #h = tf.nn.sigmoid(tf.matmul(X, w_h1)) # this is a basic mlp
        return tf.matmul(h, weights[-1]) # note that we dont take the softmax at the end because our cost fn does that for us

    def run(self, trX):
        X = tf.placeholder("float", [None, self.input_size])
        #Y = tf.placeholder("float", [None, self.output_size])

        py_x = self.model(X, self.weights)
        predict_op = tf.argmax(py_x, 1)

        time1 = time.time()
        res = self.sess.run(predict_op, feed_dict={X:trX})
        print('took:', time.time() - time1)
        return res

    def get_movement(self, trX):
        trX = np.array(trX).reshape(1, len(trX))
        return self.run(trX)[0]

#mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
#trX, trY, teX, teY = mnist.train.images, mnist.train.labels, mnist.test.images, mnist.test.labels

#cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=py_x, labels=Y)) # compute costs
#train_op = tf.train.GradientDescentOptimizer(0.05).minimize(cost) # construct an optimizer

# Launch the graph in a session
# with tf.Session() as sess:
    # saver = tf.train.Saver()

    # print("Loading variables from '{0}'.".format(CHECKPOINT_FILE))
    # saver.restore(sess, CHECKPOINT_FILE)

    # # NOTE: the iterations restart, but the weights are restored
    # # so the actual accuracy resumes from the previous epoch
    # print(range(0,len(trX),128))
    # for i in range(100):
        # for start, end in zip(range(0, len(trX), 128), range(128, len(trX)+1, 128)):
            # sess.run(train_op, feed_dict={X: trX[start:end], Y: trY[start:end]})
        # print(i, np.mean(np.argmax(teY, axis=1) ==
                         # sess.run(predict_op, feed_dict={X: teX})))
        # save_path = saver.save(sess, CHECKPOINT_FILE)
        # print("Model saved in file: %s" % save_path)

