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
        self.steps = 0
        self.go_through_boundary = True
        self.agents = [(Snake(WINDOW_SIZE[0]/ 2, WINDOW_SIZE[0]/ 2, speed, WINDOW_SIZE[0], WINDOW_SIZE[0]), NeuralNetwork((8, 20, 4))) for i in range(POPULATION_SIZE)]
        for agent in self.agents:
            snake = agent[0]
            for j in range(7):
                snake.grow()

    def consumption_check(self, snake):
        if collision(snake, self.food_stack[0]):
            return True
        else:
            return False

    def game_loop(self, key_input = None):
        self.steps += 1

        pygame.event.pump()

        self.screen.fill(self.background_color)

        if self.steps == 100:
            # 100 frames has passed now we reboot game
            pass

        # draw the food
        for food in self.food_stack:
            food.draw(self.screen)

        # draw the snake
        i = 0
        for agent in self.agents:
            snake = agent[0]
            brain = agent[1]

            head_x = snake.get_head_coor()[0]
            head_y = snake.get_head_coor()[1]
            mid_x = snake.get_mid_coor()[0]
            mid_y = snake.get_mid_coor()[1]
            tail_x = snake.get_tail_coor()[0]
            tail_y = snake.get_tail_coor()[1]
            food_x = snake.distance_from_food_x(self.food_stack[0])
            food_y = snake.distance_from_food_y(self.food_stack[0])

            #print([head_x, head_y, mid_x, mid_y, tail_x, tail_y, food_x, food_y])
            # NN will take 8 inputs and reproduce 4 outputs
            movement = np.argmax(brain.get_movement([head_x, head_y, mid_x, mid_y, tail_x, tail_y, food_x, food_y]))

            if movement == 0:
                snake.change_direction("up")
            elif movement == 1:
                snake.change_direction("down")
            elif movement == 2:
                snake.change_direction("left")
            elif movement == 3:
                snake.change_direction("right")

            end = snake.draw(self.screen, self.go_through_boundary)

            # check here if the snake ate the food
            if self.consumption_check(snake):
                self.spawn_food()
                snake.grow()

            i += 1


        pygame.display.flip()
