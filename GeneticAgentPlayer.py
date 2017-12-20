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
import math

from TFLearnNN import TFLearnNN

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
        self.remaining_agents = self.agents[:]

    def evolve_agents(self):
        current_brains = [(agent.fitness, agent.brain) for agent in self.agents]
        evolved_brains = self.ga.evolve_population(current_brains)
        self.build_agents(evolved_brains)

        #current_brains = [agent.brain for agent in self.agents]
        #self.build_agents([TFLearnNN((5, 25, 1))])

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
            if pred == -1:
                agent.body.change_direction("up")
            # right from current point of view
            elif pred == 1:
                agent.body.change_direction("down")

        elif agent.body.current_direction == "left":
            # left from current point of view
            if pred == -1:
                agent.body.change_direction("down")
            # right from current point of view
            elif pred == 1:
                agent.body.change_direction("up")

        elif agent.body.current_direction == "up":
            # left from current point of view
            if pred == -1:
                agent.body.change_direction("left")
            # right from current point of view
            elif pred == 1:
                agent.body.change_direction("right")

        elif agent.body.current_direction == "down":
            # left from current point of view
            if pred == -1:
                agent.body.change_direction("right")
            # right from current point of view
            elif pred == 1:
                agent.body.change_direction("left")



    def game_loop(self, input_key = None):
        while True:
            self.game_iteration()

    def game_iteration(self, key_input = None):
        self.steps += 1

        pygame.event.pump()

        self.screen.fill(self.background_color)

        self.display_info()

        # draw the snake
        i = 0

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
            print(self.remaining_agents, self.agents)
            self.evolve_agents()

            self.steps = 0
            self.generation_num += 1
            print("On generation {}".format(self.generation_num))

        pygame.display.flip()

    def get_input_data(self, agent):
        # all the prediction of the next frame's collision movements
        coll_pred = agent.body.self_collision_prediction()
        # get distance from the snake and food
        angle = self.get_angle(agent, self.food_stack[0])
        return [coll_pred[0], coll_pred[1], coll_pred[2], angle]

    def agent_step(self, agent):
        #input_data = self.get_input_data(agent)

        #agent.set_fitness(self.food_stack[0])

        # NN will take 8 inputs and reproduce 4 outputs
        #movement = agent.brain.get_movement(input_data)

        predictions = []
        for action in range(-1, 2):
            nn_data = self.get_input_data(agent)
            nn_data.append(action)
            nn_data = np.array(nn_data)
            # depending on previous observation what move should i generate
            predictions.append(agent.brain.get_movement(nn_data))

        movement = np.argmax(np.array(predictions)) - 1
        print(movement, predictions)
        self.map_keys(movement, agent)

    def get_angle(self, agent, food):
        head = np.array([agent.body.get_x(), agent.body.get_y()])

        segment = np.array([agent.body.body[0].get_x(), agent.body.body[0].get_y()])

        food = np.array([food.get_x(), food.get_y()])

        snake_direction = head - segment
        food_direction = food - head

        a = snake_direction / np.linalg.norm(snake_direction)
        b = food_direction / np.linalg.norm(food_direction)

        return math.atan2(a[0] * b[1] - a[1] * b[0], a[0] * b[0] + a[1] * b[1]) / math.pi

