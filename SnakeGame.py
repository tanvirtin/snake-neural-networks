import pygame
import random
from Food import Food
import time
import keyboard
from Snake import Snake
from GeneticAgentPlayer import GeneticAgentPlayer
from util import *

class SnakeGame(object):
    def __init__(self, ai_mode = False):
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.HWSURFACE)
        self.snakes_speed = SPEED

        if not ai_mode:
            self.gap = GeneticAgentPlayer(self.screen, self.snakes_speed)

        else:
            # use randomized reinforcement learning
            pass

    def ap_game_loop(self):
        return self.gap.game_loop()
