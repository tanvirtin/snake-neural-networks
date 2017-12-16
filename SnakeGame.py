import pygame
import random
from Food import Food
import time
import keyboard
from Snake import Snake
from SinglePlayer import SinglePlayer
from util import *

random.seed(42)

class SnakeGame(object):
    def __init__(self, ai_mode = False):
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.HWSURFACE)
        self.snakes_speed = SPEED

        if not ai_mode:
            self.sp = SinglePlayer(self.screen, self.snakes_speed)

    def sp_game_loop(self, action = None):
        return self.sp.game_loop(action)

if __name__ == "__main__":
    game = SnakeGame()

    direction = None

    while not keyboard.is_pressed("q"):
        if keyboard.is_pressed("w"):
            direction = "up"

        elif keyboard.is_pressed("s"):
            direction = "down"

        elif keyboard.is_pressed("a"):
            direction = "left"

        elif keyboard.is_pressed("d"):
            direction = "right"

        wall_collision, body_collision = game.sp_game_loop(direction)

        # new snake is made if this happens
        if wall_collision or body_collision:
            # if some sort of collision occurs we pause and sleep for a very short period of time indicating game being over
            time.sleep(0.5)
            game.sp.snake = Snake(50, 50, SPEED, WINDOW_SIZE[0], WINDOW_SIZE[0])
        time.sleep(0.05)
