import numpy as np

import keras
from keras.models import Model
from keras.layers import Dense
from keras.models import Sequential

class GANeuralNetwork:
    def __init__(self, dimensions, weights = None):
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

        return model

    def run(self, X):
        return self.model.predict(X)

    def get_movement(self, trX):
        trX = np.array(trX).reshape(-1, len(trX))
        return self.run(trX)[0]
