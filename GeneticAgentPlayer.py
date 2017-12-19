from Player import Player
from Snake import Snake
from GeneticAlgorithm import GeneticAlgorithm
import pygame
import random
from util import *
from collision_checker import *
import numpy as np
from GAAgent import GAAgent
from pygame.locals import *

from multiprocessing.dummy import Pool as ThreadPool

class GeneticAgentPlayer(Player):
    def __init__(self, screen, speed):
        super().__init__(screen)
        # needs to be saved as we will create a new population using the same speed
        self.ga = GeneticAlgorithm()
        self.speed = speed
        self.steps = 0
        self.go_through_boundary = False
        self.generation_num = 1

        self.build_agents()

    def build_agents(self, brains = None):
        brains = self.ga.init_population() if not brains else brains

        self.agents = [GAAgent(self.speed, brain) for brain in brains]
        # TODO: maybe more into agents constructor?
        for agent in self.agents:
            for j in range(2):
                agent.body.grow()

        self.remaining_agents = self.agents[:]

    def evolve_agents(self):
        current_brains = [(agent.fitness, agent.brain) for agent in self.agents]
        evolved_brains = self.ga.evolve_population(current_brains)
        self.build_agents(evolved_brains)

    def consumption_check(self, snake):
        if collision(snake, self.food_stack[0]):
            return True
        else:
            return False

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

    def map_keys(self, pred, agent):
        if agent.body.current_direction == "right":
            # left from current point of view
            if pred == 0:
                agent.body.change_direction("up")
            # right from current point of view
            elif pred == 2:
                agent.body.change_direction("down")

        elif agent.body.current_direction == "left":
            # left from current point of view
            if pred == 0:
                agent.body.change_direction("down")
            # right from current point of view
            elif pred == 2:
                agent.body.change_direction("up")

        elif agent.body.current_direction == "up":
            # left from current point of view
            if pred == 0:
                agent.body.change_direction("left")
            # right from current point of view
            elif pred == 2:
                agent.body.change_direction("right")

        elif agent.body.current_direction == "down":
            # left from current point of view
            if pred == 0:
                agent.body.change_direction("right")
            # right from current point of view
            elif pred == 2:
                agent.body.change_direction("left")



    def game_loop(self, key_input = None):
        self.steps += 1

        pygame.event.pump()

        self.screen.fill(self.background_color)

        self.display_info()

        # draw the snake
        i = 0

        # pool = ThreadPool(4)
        # results = pool.map(self.agent_step, self.remaining_agents)
        # #close the pool and wait for the work to finish
        # pool.close()
        # pool.join()

        for agent in self.remaining_agents:
            self.agent_step(agent)

            end = agent.body.draw(self.screen, self.go_through_boundary)

            if (end):
                agent.dead = True
                self.remaining_agents.remove(agent)
                print("An agent has died!")
                if len(self.remaining_agents) == 0:
                    break

            # check here if the snake ate the food
            if self.consumption_check(agent.body):
                self.spawn_food()
                agent.body.grow()
                # agent gets a point if he can eat the food
                agent.score += 1
                print("A snake ate a food!")
            i += 1

        if self.steps == 200 or len(self.remaining_agents) == 0:
            self.evolve_agents()

            self.steps = 0
            self.generation_num += 1
            print("On generation {}".format(self.generation_num))

        pygame.display.flip()

    def get_input_data(self, agent):
        # all the prediction of the next frame's collision movements
        coll_pred = agent.body.self_collision_prediction()
        # get distance from the snake and food
        distance_from_food = agent.body.distance_from_food(self.food_stack[0])
        #angle = self.get_angle()
        return [coll_pred[0], coll_pred[1], coll_pred[2], distance_from_food]

    def agent_step(self, agent):

        input_data = self.get_input_data(agent)


        agent.set_fitness(self.food_stack[0])

        # NN will take 8 inputs and reproduce 4 outputs
        movement = agent.brain.get_movement(input_data)

        self.map_keys(movement, agent)
