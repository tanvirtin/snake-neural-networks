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

class AgentPlayer(Player):
    def __init__(self, screen, speed):
        super().__init__(screen)
        # needs to be saved as we will create a new population using the same speed
        self.speed = speed
        self.steps = 0
        self.go_through_boundary = True
        self.agents = [Agent(self.speed) for i in range(POPULATION_SIZE)]
        for agent in self.agents:
            for j in range(2):
                agent.body.grow()

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

            # check here if the snake ate the food
            if self.consumption_check(agent.body):
                self.spawn_food()
                agent.body.grow()
                # agent gets a point if he can eat the food
                agent.points += 1

            i += 1

        if self.steps == 100:
            self.create_new_population()


        pygame.display.flip()
