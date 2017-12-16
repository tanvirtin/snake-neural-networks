import pygame
import random
from Food import Food
import time
import keyboard
from Snake import Snake
from SinglePlayer import SinglePlayer
from util import *

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
        if keyboard.is_pressed("up"):
            direction = "up"

        elif keyboard.is_pressed("down"):
            direction = "down"

        elif keyboard.is_pressed("left"):
            direction = "left"

        elif keyboard.is_pressed("right"):
            direction = "right"

        start = time.time()
        end = game.sp_game_loop(direction)
        finish = time.time()


        # new snake is made if this happens
        if end:
            # if some sort of collision occurs we pause and sleep for a very short period of time indicating game being over
            time.sleep(0.5)
            game.sp.snake = Snake(WINDOW_SIZE[0] / 2, WINDOW_SIZE[0] / 2, SPEED, WINDOW_SIZE[0], WINDOW_SIZE[0])
        time.sleep(0.05)
