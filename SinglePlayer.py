from Player import Player
from Snake import Snake
import pygame
import random
from util import *
import cv2
from collision_checker import *
import sys
import numpy as np
import math

class SinglePlayer(Player):
    def __init__(self, screen, speed):
        super().__init__(screen)
        # takes in x, y of the snake and the speed of the snake
        self.snakes_speed = speed
        self.snake = Snake(WINDOW_SIZE[0] / 2, WINDOW_SIZE[0] / 2, self.snakes_speed, WINDOW_SIZE[0], WINDOW_SIZE[0])
        self.go_through_boundary = True

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

    def map_keys(self, pred):
        if self.snake.current_direction == "right":
            # left from current point of view
            if pred == -1:
                self.snake.change_direction("up")
            # right from current point of view
            elif pred == 1:
                self.snake.change_direction("down")

        elif self.snake.current_direction == "left":
            # left from current point of view
            if pred == -1:
                self.snake.change_direction("down")
            # right from current point of view
            elif pred == 1:
                self.snake.change_direction("up")

        elif self.snake.current_direction == "up":
            # left from current point of view
            if pred == -1:
                self.snake.change_direction("left")
            # right from current point of view
            elif pred == 1:
                self.snake.change_direction("right")

        elif self.snake.current_direction == "down":
            # left from current point of view
            if pred == -1:
                self.snake.change_direction("right")
            # right from current point of view
            elif pred == 1:
                self.snake.change_direction("left")

    def display_info(self):
        pygame.font.init()

        default_font = pygame.font.get_default_font()
        font_renderer = pygame.font.Font(default_font, 10)

        # To create a surface containing `Some Text`
        label = font_renderer.render("Score - {}".format(self.snake.score), 1, (0,0,0)) # RGB Color
        self.screen.blit(label, (0,0))

        # draw the food
        for food in self.food_stack:
            food.draw(self.screen)

    def get_angle(self):
        x1 = self.snake.get_x()
        y1 = self.snake.get_y()

        x2 = self.food_stack[0].get_x()
        y2 = self.food_stack[0].get_y()

        x1 /= np.linalg.norm(np.array([x1, y1]))
        y1 /= np.linalg.norm(np.array([x1, y1]))

        x2 /= np.linalg.norm(np.array([x2, y2]))
        y2 /= np.linalg.norm(np.array([x2, y2]))

        # (2 * math.pi is to normalize the angle)
        return math.atan2(x1 * y2 - y1 * x2, x1 * x2 + y1 * y2) / math.pi

    def get_angle_2(self):
        x1 = self.snake.get_x()
        y1 = self.snake.get_y()

        x2 = self.food_stack[0].get_x()
        y2 = self.food_stack[0].get_y()

        return math.atan2(y1 - y2, x1 - x2) / math.pi

    def game_loop(self, key_input = None):
        pygame.event.pump()

        self.screen.fill(self.background_color)

        self.display_info()

        for food in self.food_stack:
            food.draw(self.screen)

        if not key_input:
            end = self.snake.draw(self.screen, self.go_through_boundary)

        else:
            self.snake.change_direction(key_input)

            end = self.snake.draw(self.screen, self.go_through_boundary)

        print(self.get_angle())

        # check here if the snake ate the food
        if self.consumption_check():

            self.spawn_food()

            # finally we grow the snake as well by adding a new segment to the snake's body
            self.snake.grow()

        pygame.display.flip()

        #print("Distance from food: {}".format(self.snake.distance_from_food(self.food_stack[0])))

        return end
