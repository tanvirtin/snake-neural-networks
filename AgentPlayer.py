from Player import Player
from Snake import Snake
import pygame
import random
from util import *
import cv2
from collision_checker import *
from NeuralNetwork import NeuralNetwork
import numpy as np
from Agent import Agent
from pygame.locals import *

class AgentPlayer(Player):
    def __init__(self, screen, speed):
        super().__init__(screen)
        # needs to be saved as we will create a new population using the same speed
        self.speed = speed
        self.steps = 0
        self.go_through_boundary = False
        self.agents = [Agent(self.speed) for i in range(POPULATION_SIZE)]
        for agent in self.agents:
            for j in range(2):
                agent.body.grow()
        self.generation_num = 1

    def consumption_check(self, snake):
        if collision(snake, self.food_stack[0]):
            return True
        else:
            return False

    def create_new_population(self):
        self.agents = [Agent(self.speed) for i in range(POPULATION_SIZE)]
        for agent in self.agents:
            for j in range(2):
                agent.body.grow()

    def display_info(self):
        pygame.font.init()

        default_font = pygame.font.get_default_font()
        font_renderer = pygame.font.Font(default_font, 10)

        # To create a surface containing `Some Text`
        label = font_renderer.render("Generation - {}".format(self.generation_num), 1, (0,0,0)) # RGB Color
        self.screen.blit(label, (0,0))

        # draw the food
        for food in self.food_stack:
            food.draw(self.screen)


    def game_loop(self, key_input = None):
        self.steps += 1

        pygame.event.pump()

        self.screen.fill(self.background_color)

        self.display_info()

        # draw the snake
        i = 0

        for agent in self.agents:
            head_x = agent.body.get_head_coor()[0]
            head_y = agent.body.get_head_coor()[1]
            mid_x = agent.body.get_mid_coor()[0]
            mid_y = agent.body.get_mid_coor()[1]
            tail_x = agent.body.get_tail_coor()[0]
            tail_y = agent.body.get_tail_coor()[1]
            food_x = agent.body.distance_from_food_x(self.food_stack[0])
            food_y = agent.body.distance_from_food_y(self.food_stack[0])

            # NN will take 8 inputs and reproduce 4 outputs
            movement = np.argmax(agent.brain.get_movement([head_x, head_y, mid_x, mid_y, tail_x, tail_y, food_x, food_y]))

            if movement == 0:
                agent.body.change_direction("up")
            elif movement == 1:
                agent.body.change_direction("down")
            elif movement == 2:
                agent.body.change_direction("left")
            elif movement == 3:
                agent.body.change_direction("right")

            end = agent.body.draw(self.screen, self.go_through_boundary)

            if (end):
                agent.dead = True
                self.agents.remove(agent)
                print("An agent has died!")
                if len(self.agents) == 0:
                    self.create_new_population()
                    self.steps = 0
                    self.generation_num += 1
                    return

            # check here if the snake ate the food
            if self.consumption_check(agent.body):
                self.spawn_food()
                agent.body.grow()
                # agent gets a point if he can eat the food
                agent.score += 1
                print("A snake ate a food!")
            i += 1

        if self.steps == 500:
            self.create_new_population()
            self.steps = 0
            self.generation_num += 1
            print("On generation {}".format(self.generation_num))

        pygame.display.flip()
