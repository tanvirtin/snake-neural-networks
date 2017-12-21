import pygame
import random
import time
from Snake import Snake
from GeneticAgentPlayer import GeneticAgentPlayer
from RLAgentPlayer import RLAgentPlayer
from util import *
from SinglePlayer import SinglePlayer

class SnakeGame(object):
    def __init__(self, reinforcement_learning = False, use_keras = True):
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.HWSURFACE)
        self.snakes_speed = SPEED
        self.reinforcement_learning = reinforcement_learning

        if not self.reinforcement_learning:
            self.player = GeneticAgentPlayer(self.screen, self.snakes_speed)
        else:
            self.player = RLAgentPlayer(self.screen, self.snakes_speed, use_keras)

    def game_loop(self):
        return self.player.game_loop()

    def gather_data(self):
        if self.reinforcement_learning:
            self.player.gather_training_data()

    def train_agent(self):
        if self.reinforcement_learning:
            self.player.train_agent()

    def test_agent(self, dataset_games = "Some number of games"):
        if self.reinforcement_learning:
            self.player.test_agent(dataset_games)
