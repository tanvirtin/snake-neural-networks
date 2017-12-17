import pygame
import random
from Food import Food
import time
import keyboard
from Snake import Snake
from AgentPlayer import AgentPlayer
from util import *

class SnakeGame(object):
    def __init__(self, ai_mode = False):
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.HWSURFACE)
        self.snakes_speed = SPEED

        if not ai_mode:
            self.ap = AgentPlayer(self.screen, self.snakes_speed)

    def ap_game_loop(self):
        return self.ap.game_loop()

if __name__ == "__main__":
    game = SnakeGame()

    while not keyboard.is_pressed("q"):
        game.ap_game_loop()
        time.sleep(0.05)
