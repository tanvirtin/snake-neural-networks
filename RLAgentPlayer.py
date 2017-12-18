from Player import Player
from Snake import Snake
import pygame
import random
from util import *
import cv2
from collision_checker import *
import sys

class RLAgentPlayer(Player):
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

    def game_loop(self, key_input = None):
        pygame.event.pump()

        self.screen.fill(self.background_color)

        self.display_info()

        for food in self.food_stack:
            food.draw(self.screen)

        print(self.snake.self_collision_prediction())

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

        pygame.display.flip()

        #print("Distance from food: {}".format(self.snake.distance_from_food(self.food_stack[0])))

        return end
