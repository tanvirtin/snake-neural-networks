import pygame
import random
import time
from Snake import Snake
from GeneticAgentPlayer import GeneticAgentPlayer
from RLAgentPlayer import RLAgentPlayer
from util import *
from SinglePlayer import SinglePlayer

class SnakeGame(object):
    def __init__(self, reinforcement_learning = False, use_keras = True, pre_trained = True, total_training_games = TOTAL_TRAINING_GAMES, population_size = 10):
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.HWSURFACE)
        self.snakes_speed = SPEED
        self.reinforcement_learning = reinforcement_learning

        if not self.reinforcement_learning:
            self.player = GeneticAgentPlayer(self.screen, self.snakes_speed, pop_size = population_size)
        else:
            self.player = RLAgentPlayer(self.screen, self.snakes_speed, use_keras, pre_trained, total_training_games)

    def game_loop(self):
        return self.player.game_loop()

    def gather_data(self):
        if self.reinforcement_learning:
            self.player.gather_training_data()

    def train_agent(self, gen_num = 20):
        self.player.train_agent(gen_num)

    def test_agent(self, dataset_games = "Some number of games"):
        if self.reinforcement_learning:
            self.player.test_agent(dataset_games)
        else:
            self.player.test_agent()
