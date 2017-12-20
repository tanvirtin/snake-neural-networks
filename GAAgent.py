from Snake import Snake
from util import *

LENGTH_WEIGHT = 100
DISTANCE_WEIGHT = 50

class GAAgent(object):
    def __init__(self, speed, brain, size=2):
        self.body = Snake(WINDOW_SIZE[0]/ 2, WINDOW_SIZE[0]/ 2, speed, WINDOW_SIZE[0], WINDOW_SIZE[0])
        self.brain = brain
        self.dead = False
        self.score = 0
        self.fitness = 0
        self.grow(size)

    def grow(self, size):
        for _ in range(size):
            self.body.grow()

    def set_fitness(self, food):
        distance_from_food = self.body.distance_from_food(food)
        self.fitness = self.body.length() * LENGTH_WEIGHT + distance_from_food * DISTANCE_WEIGHT
