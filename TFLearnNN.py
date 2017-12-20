# import tflearn
import numpy as np

import keras
from keras.models import Model
from keras.layers import Dense
from keras.models import Sequential

# import tflearn
# from tflearn.layers.core import input_data, fully_connected

class TFLearnNN:
    def __init__(self, dimensions, weights = None):
        #self.input_size = dimensions[0]
        #self.output_size = dimensions[-1]
        #self.dimensions = list(zip(dimensions[:-1], dimensions[1:]))
        self.dimensions = dimensions

        self.model = self.build_model()
        # set weights if provided
        if weights is not None:
            self.set_weights(weights)

    def shape(self):
        return np.array(self.weights).shape

    # def set_weights(self, weights):
        # if len(self.layers) != len(weights):
            # print("ERROR: Weight mismatch")
            # return
        # for w, l in zip(weights, self.layers):
            # self.model.set_weights(l.W, w[0])
            # self.model.set_weights(l.b, w[1])

    def set_weights(self, weights):
        if len(self.model.layers) != len(weights):
            print("ERROR: Weight mismatch")
            return
        for w, l in zip(weights, self.model.layers):
            l.set_weights(w)

    # def weights(self):
        # return [[self.model.get_weights(l.W), self.model.get_weights(l.b)]
                    # for l in self.layers]
    def weights(self):
        return [layer.get_weights() for layer in self.model.layers]

    def build_model(self):
        # input_layer = tflearn.input_data(shape=[None, self.dimensions[0]])
        # dense1 = tflearn.fully_connected(input_layer, self.dimensions[1], activation='leaky_relu')
        # dense2 = tflearn.fully_connected(dense1, self.dimensions[2], activation='leaky_relu')

        # Regression using SGD with learning rate decay and Top-3 accuracy
        # sgd = tflearn.SGD(learning_rate=0.1, lr_decay=0.96, decay_step=1000)
        # top_k = tflearn.metrics.Top_k(3)
        # net = tflearn.regression(dense2, optimizer=sgd, metric=top_k, loss='categorical_crossentropy')

        # return tflearn.DNN(dense2,tensorboard_verbose=0)

        model = Sequential()
        model.add(
                Dense(
                    self.dimensions[1],
                    input_dim = self.dimensions[0],
                    activation = 'sigmoid',
                    kernel_initializer=keras.initializers.RandomUniform(minval=-1, maxval=1),
                    bias_initializer=keras.initializers.RandomUniform(minval=-1, maxval=1),
                )
        )
        model.add(
            Dense(
                self.dimensions[2],
                activation = 'sigmoid',
                kernel_initializer=keras.initializers.RandomUniform(minval=-1, maxval=1),
                bias_initializer=keras.initializers.RandomUniform(minval=-1, maxval=1),
            )
        )

        # input_layer = input_data(shape=[None, self.dimensions[0]], name="input")
        # dense1 = fully_connected(input_layer, self.dimensions[1], activation="relu")
        # dense2 = fully_connected(dense1, self.dimensions[2], activation="linear")

        # model = tflearn.DNN(dense2)
        # layers = [dense1, dense2]

        return model

    def run(self, X):
        return self.model.predict(X)

    def get_movement(self, trX):
        trX = np.array(trX).reshape(-1, len(trX))
        return self.run(trX)[0]
        #return np.argmax(res)
