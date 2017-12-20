from Snake import Snake
from util import *
import tflearn
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression
import numpy as np

class RLAgent(object):
    def __init__(self, speed):
        self.speed = speed
        self.body = Snake(WINDOW_SIZE[0] / 2, WINDOW_SIZE[0] / 2, self.speed, WINDOW_SIZE[0], WINDOW_SIZE[0])
        for _ in range(3):
            self.body.grow()
        self.brain = self.__create_brain(1e-2)

    # creates a new body when the snake dies
    def create_new_body(self):
        self.body = Snake(WINDOW_SIZE[0] / 2, WINDOW_SIZE[0] / 2, self.speed, WINDOW_SIZE[0], WINDOW_SIZE[0])
        for _ in range(3):
            self.body.grow()

    # the tiny powerhouse of the snake is created
    def __create_brain(self, learning_rate):
        network = input_data(shape = [None, 5, 1], name = "input")
        network = fully_connected(network, 25, activation = "relu")
        network = fully_connected(network, 1, activation = "linear")
        network = regression(network, optimizer = "adam", learning_rate = learning_rate, loss = "mean_square", name = "target")
        model = tflearn.DNN(network)
        return model

    # learns from the training_data provided
    def learn(self, training_data):
        inputs = np.array([i[0] for i in training_data]).reshape(-1, 5, 1)
        outputs = np.array([i[1] for i in training_data]).reshape(-1, 1)
        self.brain.fit(inputs, outputs, n_epoch = 3, shuffle = True)
