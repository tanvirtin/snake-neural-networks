from Snake import Snake
from util import *
import numpy as np
from RLNeuralNetwork import NeuralNetwork
from RLNeuralNetworkKeras import KerasNeuralNetwork
from tqdm import tqdm

class RLAgent(object):
    def __init__(self, speed, use_keras = True):
        self.speed = speed
        self.body = Snake(WINDOW_SIZE[0] / 2, WINDOW_SIZE[0] / 2, self.speed, WINDOW_SIZE[0], WINDOW_SIZE[0])
        for _ in range(3):
            self.body.grow()

        if not use_keras:
            self.brain = self.__create_brain((5, 200, 200, 1), 1e-2)
        else:
            self.brain = self.__create_brain_keras((5, 75, 1))

    # creates a new body when the snake dies
    def create_new_body(self):
        self.body = Snake(WINDOW_SIZE[0] / 2, WINDOW_SIZE[0] / 2, self.speed, WINDOW_SIZE[0], WINDOW_SIZE[0])
        for _ in range(3):
            self.body.grow()

    def __create_brain_keras(self, dimensions):
        return KerasNeuralNetwork(dimensions)

    def __create_brain(self, dimensions, learning_rate):
        return NeuralNetwork(dimensions, learning_rate)

    def predict(self, input_data):
        return self.brain.query(input_data)

    def learn(self, training_data):
        batches = 32
        epochs = 15
        self.brain.fit(training_data, batches, epochs)
