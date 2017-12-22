import pygame
import random
import time
from Snake import Snake
from GeneticAgentPlayer import GeneticAgentPlayer
from RLAgentPlayer import RLAgentPlayer
from util import *
from SinglePlayer import SinglePlayer

class SnakeGame(object):
    def __init__(self, reinforcement_learning = False, use_keras = True, pre_trained = True, population_size = 10):
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.HWSURFACE)
        self.snakes_speed = SPEED
        self.reinforcement_learning = reinforcement_learning

        if not self.reinforcement_learning:
            self.player = GeneticAgentPlayer(self.screen, self.snakes_speed, pop_size = population_size)
        else:
            self.player = RLAgentPlayer(self.screen, self.snakes_speed, use_keras, pre_trained)

    def game_loop(self):
        return self.player.game_loop()

    def gather_data(self, num_data):
        if self.reinforcement_learning:
            self.player.gather_training_data(num_data)

    def train_agent(self, gen_num = 20):
        if not self.reinforcement_learning:
            self.player.train_agent(gen_num)
        else:
            self.player.train_agent()

    def test_agent(self, dataset_games = "some number of games"):
        if self.reinforcement_learning:
            self.player.test_agent(dataset_games)
        else:
            self.player.test_agent(dataset_games)
