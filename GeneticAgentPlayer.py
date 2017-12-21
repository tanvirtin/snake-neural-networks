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

class GeneticAgentPlayer(Player):
    def __init__(self, screen, speed):
        super().__init__(screen)
        # needs to be saved as we will create a new population using the same speed
        self.ga = GeneticAlgorithm()
        self.speed = speed
        self.high_score = 0
        self.go_through_boundary = False

    def build_agents(self, brains = None):
        brains = self.ga.init_population() if not brains else brains
        return [GAAgent(self.speed, brain) for brain in brains]

    def should_reset(self, prev_agents):
        poor_agents = [a for a in prev_agents if a.body.length() == INIT_SNAKE_LENGTH + 1]
        return len(poor_agents) == len(prev_agents)

    def evolve_agents(self, prev_agents):
        if self.should_reset(prev_agents):
            print('No good snakes, recreating')
            return self.build_agents()

        current_brains = [(agent.fitness, agent.brain) for agent in prev_agents]
        evolved_brains = self.ga.evolve_population(current_brains)
        return self.build_agents(evolved_brains)

    def consumption_check(self, snake):
        if collision(snake, self.food_stack[0]):
            return True
        else:
            return False


    def display_info(self, high_score, current_generation):
        pygame.font.init()

        default_font = pygame.font.get_default_font()
        font_renderer = pygame.font.Font(default_font, 10)

        # To create a surface containing `Some Text`
        label = font_renderer.render("Generation - {}, High score: {}".format(current_generation, high_score), 1, (0,0,0)) # RGB Color
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

    def save_best_agent(self, agents):
        current_brains = [(agent.fitness, agent.brain) for agent in agents]
        self.ga.save_best_agent(current_brains)

    def game_loop(self, num_iterations = 100):
        # create agent from saved model
        networks = [self.ga.load_model()]
        high_score = 0
        sum_score = 0
        for iteration in range(1, num_iterations+1):
            agents = self.build_agents(networks)
            remaining_agents = agents[:]

            best_score, high_score = self.evolve_loop(remaining_agents, iteration, high_score, num_steps=1000)
            sum_score += best_score

            print("On game {}".format(iteration))

        average_score = sum_score / num_iterations
        data_prints = [
            "Neural Network played {}\n".format(num_iterations),
            "Highest Score in {} games: {}\n".format(num_iterations, high_score),
            "Average Score in {} games: {}\n".format(num_iterations, average_score)
         ]

        with open("test-result.txt", "a") as myfile:
            for prints in data_prints:
                myfile.write(prints)
                print(prints)

    def train_agent(self, num_iterations = 10):
        # build initial agents
        agents = self.build_agents()
        high_score = 0
        for iteration in range(1, num_iterations+1):
            remaining_agents = agents[:]

            best_score, high_score = self.evolve_loop(remaining_agents, iteration, high_score)

            # evolve agents after loop
            agents = self.evolve_agents(agents)
            print("On generation {}".format(iteration))
        # save the model of the best agent
        print('Saving best agent')
        self.save_best_agent(agents)

    def evolve_loop(self, remaining_agents, current_generation, high_score, num_steps = 200):
        best_score = 0
        for steps in range(num_steps):
            best_score = self.game_iteration(remaining_agents, current_generation, best_score, high_score)
            if best_score > high_score:
                high_score = best_score
            if len(remaining_agents) == 0:
                break
        return best_score, high_score

    def game_iteration(self, remaining_agents, current_generation, best_score, high_score):
        pygame.event.pump()

        self.screen.fill(self.background_color)

        self.display_info(high_score, current_generation)

        for agent in remaining_agents:
            self.agent_step(agent)

            end = agent.body.draw(self.screen, self.go_through_boundary)

            if (end):
                agent.dead = True
                remaining_agents.remove(agent)
                print("An agent has died!")
                if len(remaining_agents) == 0:
                    self.spawn_food()
                    break

            # check here if the snake ate the food
            if self.consumption_check(agent.body):
                self.spawn_food()
                agent.body.grow()
                # agent gets a point if he can eat the food
                agent.score += 1
                if agent.score > best_score:
                    best_score = agent.score
                print("A snake ate a food!")

        pygame.display.flip()
        return best_score

    def get_input_data(self, agent):
        # all the prediction of the next frame's collision movements
        coll_pred = agent.body.self_collision_prediction()
        # get distance from the snake and food
        angle = self.get_angle(agent, self.food_stack[0])
        return [coll_pred[0], coll_pred[1], coll_pred[2], angle]

    def agent_step(self, agent):
        agent.set_fitness(self.food_stack[0])

        predictions = []
        for action in range(-1, 2):
            nn_data = self.get_input_data(agent)
            nn_data.append(action)
            nn_data = np.array(nn_data)
            # depending on previous observation what move should i generate
            predictions.append(agent.brain.get_movement(nn_data))

        movement = np.argmax(np.array(predictions)) - 1
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
