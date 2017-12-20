from keras.models import Sequential
from keras.layers import Dense, Activation
import numpy as np

class KerasNeuralNetwork(object):
    def __init__(self, dimensions):
        self.model = Sequential()
        self.model.add(Dense(dimensions[1], activation = 'relu', input_dim = dimensions[0]))
        self.model.add(Dense(dimensions[-1], activation = 'sigmoid'))
        self.model.compile(optimizer = 'rmsprop', loss = 'mse')


    def query(self, input_data):
        input_data = np.array(input_data).reshape(-1, 5)
        return self.model.predict(input_data)

    def fit(self, training_data, num_batches, num_epochs):
        inputs = np.array([i[0] for i in training_data]).reshape(-1, 5)
        outputs = np.array([i[1] for i in training_data]).reshape(-1, 1)
        self.model.fit(inputs, outputs, epochs = num_epochs, batch_size = num_batches)
