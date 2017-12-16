from Player import Player
from Snake import Snake
import pygame
import random
from util import *
import cv2
from collision_checker import *
import sys

class SinglePlayer(Player):
    def __init__(self, screen, speed):
        super().__init__(screen)
        # takes in x, y of the snake and the speed of the snake
        self.snakes_speed = speed
        self.snake = Snake(50, 50, self.snakes_speed, WINDOW_SIZE[0], WINDOW_SIZE[0])
        self.go_through_boundary = False

    def consumption_check(self):
        if collision(self.snake, self.food_stack[0]):
            return True
        else:
            return False

    def get_game_pixels(self):
        # get the game pixel
        pixels = pygame.surfarray.array3d(pygame.display.get_surface())
        # # convert pixel into greyscale image with only 1 channel
        # cv2 is far more superior then any other library in image manipulation
        pixels = cv2.cvtColor(pixels, cv2.COLOR_BGR2GRAY) / 255

        return pixels

    def game_loop(self, key_input = None):
        pygame.event.pump()

        self.screen.fill(self.background_color)

        for food in self.food_stack:
            food.draw(self.screen)

        if not key_input:
            end = self.snake.draw(self.screen, self.go_through_boundary)

        else:
            self.snake.change_direction(key_input)
            end = self.snake.draw(self.screen, self.go_through_boundary)

        # check here if the snake ate the food
        if self.consumption_check():

            self.spawn_food()

            # finally we grow the snake as well by adding a new segment to the snake's body
            self.snake.grow()
            sys.exit()

        pygame.display.flip()

        print("Distance from food: {}".format(self.snake.distance_from_food(self.food_stack[0])))

        return end
