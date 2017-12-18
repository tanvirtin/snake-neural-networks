from NeuralNetwork import NeuralNetwork
from Snake import Snake
from util import *

class GAAgent(object):
    def __init__(self, speed):
        self.body = Snake(WINDOW_SIZE[0]/ 2, WINDOW_SIZE[0]/ 2, speed, WINDOW_SIZE[0], WINDOW_SIZE[0])
        self.brain = NeuralNetwork((8, 10, 4))
        self.dead = False
        self.score = 0
        self.fitness = 0
