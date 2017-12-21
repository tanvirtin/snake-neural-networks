from Snake import Snake
from util import *
import numpy as np
import math

LENGTH_WEIGHT = 10000
ANGLE_WEIGHT = 5000
DISTANCE_WEIGHT = 50

class GAAgent(object):
    def __init__(self, speed, brain, size=INIT_SNAKE_LENGTH):
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
        angle = self.get_angle(self, food)
        self.fitness = self.body.length() * LENGTH_WEIGHT + distance_from_food * DISTANCE_WEIGHT + (ANGLE_WEIGHT * angle)


    def get_angle(self, agent, food):
        head = np.array([agent.body.get_x(), agent.body.get_y()])

        segment = np.array([agent.body.body[0].get_x(), agent.body.body[0].get_y()])

        food = np.array([food.get_x(), food.get_y()])

        snake_direction = head - segment
        food_direction = food - head

        a = snake_direction / np.linalg.norm(snake_direction)
        b = food_direction / np.linalg.norm(food_direction)

        return math.atan2(a[0] * b[1] - a[1] * b[0], a[0] * b[0] + a[1] * b[1]) / math.pi
