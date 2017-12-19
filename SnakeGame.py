import pygame
import random
import time
from Snake import Snake
from GeneticAgentPlayer import GeneticAgentPlayer
from RLAgentPlayer import RLAgentPlayer
from util import *
from SinglePlayer import SinglePlayer

class SnakeGame(object):
    def __init__(self, reinforcement_learning = False):
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.HWSURFACE)
        self.snakes_speed = SPEED
        self.reinforcement_learning = reinforcement_learning

        if not self.reinforcement_learning:
            self.player = GeneticAgentPlayer(self.screen, self.snakes_speed)
        else:
            self.player = RLAgentPlayer(self.screen, self.snakes_speed)

    def game_loop(self, key_input = None):
        return self.player.game_loop(key_input)

    def prepare_players(self):
        if self.reinforcement_learning:
            self.player.train_agent()
