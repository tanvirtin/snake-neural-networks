from Player import Player
from Snake import Snake
import pygame
import random
from util import *
import cv2
from collision_checker import *
from NeuralNetwork import NeuralNetwork
import numpy as np

class AgentPlayer(Player):
    def __init__(self, screen, speed):
        super().__init__(screen)
        self.go_through_boundary = True
        self.agents = [(Snake(WINDOW_SIZE[0]/ 2, WINDOW_SIZE[0]/ 2, speed, WINDOW_SIZE[0], WINDOW_SIZE[0]), NeuralNetwork((1, 5, 4))) for i in range(POPULATION_SIZE)]

    def consumption_check(self, snake):
        if collision(snake, self.food_stack[0]):
            return True
        else:
            return False

    def game_loop(self, key_input = None):
        pygame.event.pump()

        self.screen.fill(self.background_color)

        # draw the food
        for food in self.food_stack:
            food.draw(self.screen)

        # draw the snake
        for agent in self.agents:
            # the direction of the snake depends on the neural network
            movement = np.argmax(agent[1].get_movement(random.random()))
            print(movement)
            if movement == 0:
                agent[0].change_direction("up")
            elif movement == 1:
                agent[0].change_direction("down")
            elif movement == 2:
                agent[0].change_direction("left")
            elif movement == 3:
                agent[0].change_direction("right")

            end = agent[0].draw(self.screen, self.go_through_boundary)

            # check here if the snake ate the food
            if self.consumption_check(agent[0]):
                self.spawn_food()
                agent[0].grow()

        pygame.display.flip()
