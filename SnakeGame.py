import pygame
import random
from Food import Food
import time
import keyboard
from Snake import Snake
from GeneticAgentPlayer import GeneticAgentPlayer
from RLAgentPlayer import RLAgentPlayer
from util import *

class SnakeGame(object):
    def __init__(self, reinforcement_learning = False):
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.HWSURFACE)
        self.snakes_speed = SPEED

        if not reinforcement_learning:
            self.player = GeneticAgentPlayer(self.screen, self.snakes_speed)
        else:
            self.player = RLAgentPlayer(self.screen, self.snakes_speed)

    def ga_game_loop(self):
        return self.player.game_loop()

    def rl_game_loop(self, key_input = None):
        return self.player.game_loop(key_input)

    def prepare_rl_player(self):
        self.player.train_agent()
