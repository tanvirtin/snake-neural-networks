from Player import Player
from Snake import Snake
import pygame
import random
from util import *
import cv2
from collision_checker import *
from NeuralNetwork import NeuralNetwork

class AgentPlayer(Player):
    def __init__(self, screen, speed):
        super().__init__(screen)
        self.step = 0
        self.go_through_boundary = True
        self.snakes = [Snake(WINDOW_SIZE[0]/ 2, WINDOW_SIZE[0]/ 2, speed, WINDOW_SIZE[0], WINDOW_SIZE[0]) for i in range(POPULATION_SIZE)]
        self.brains = [NeuralNetwork((1, 5, 4)) for i in range(POPULATION_SIZE)]

    def consumption_check(self):
        if collision(self.snake, self.food_stack[0]):
            return True
        else:
            return False

    def game_loop(self, key_input = None):
        self.step += 1

        if self.step % 150 == 0:
            print("150 steps taken")

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
            self.step = 0

        pygame.display.flip()

        # print("Distance from food: {}".format(self.snake.distance_from_food_x(self.food_stack[0])))

        return end
