# import tflearn
import numpy as np

import keras
from keras.models import Model
from keras.layers import Dense
from keras.models import Sequential

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

    def set_weights(self, weights):
        if len(self.model.layers) != len(weights):
            print("ERROR: Weight mismatch")
            return
        for w, l in zip(weights, self.model.layers):
            l.set_weights(w)

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
        model.add(Dense(self.dimensions[1], input_dim = self.dimensions[0], activation = 'sigmoid', bias_initializer='random_normal'))
        model.add(Dense(self.dimensions[2], activation = 'sigmoid'))
        
        return model

    def run(self, X):
        return self.model.predict(X)

    def get_movement(self, trX):
        trX = np.array(trX).reshape(-1, len(trX))
        res = self.run(trX)[0]
        return np.argmax(res)
