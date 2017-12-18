from Player import Player
from Snake import Snake
import pygame
import random
from util import *
from collision_checker import *
from RLAgent import RLAgent
import sys
import numpy as np
import math

class RLAgentPlayer(Player):
    def __init__(self, screen, speed):
        super().__init__(screen)
        # takes in x, y of the snake and the speed of the snake
        self.agent = RLAgent(speed)
        self.go_through_boundary = True
        # total number of games required to train
        self.total_training_games = 10
        # number of frames rendered to collect the data
        self.goal_steps = 2000

    def consumption_check(self):
        if collision(self.agent.body, self.food_stack[0]):
            return True
        else:
            return False

    def display_info(self):
        pygame.font.init()

        default_font = pygame.font.get_default_font()
        font_renderer = pygame.font.Font(default_font, 10)

        # To create a surface containing `Some Text`
        label = font_renderer.render("Score - {}".format(self.agent.body.score), 1, (0,0,0)) # RGB Color
        self.screen.blit(label, (0,0))

        # draw the food
        for food in self.food_stack:
            food.draw(self.screen)

    def get_angle(self):
        x1 = self.agent.body.get_x()
        y1 = self.agent.body.get_y()

        x2 = self.food_stack[0].get_x()
        y2 = self.food_stack[0].get_y()

        return math.atan2(y2 - y1, x2 - x1)


    def map_keys(self, pred):
        if self.agent.body.current_direction == "right":
            # left from current point of view
            if pred == -1:
                self.agent.body.change_direction("up")
            # right from current point of view
            elif pred == 1:
                self.agent.body.change_direction("down")

        elif self.agent.body.current_direction == "left":
            # left from current point of view
            if pred == -1:
                self.agent.body.change_direction("down")
            # right from current point of view
            elif pred == 1:
                self.agent.body.change_direction("up")

        elif self.agent.body.current_direction == "up":
            # left from current point of view
            if pred == -1:
                self.agent.body.change_direction("left")
            # right from current point of view
            elif pred == 1:
                self.agent.body.change_direction("right")

        elif self.agent.body.current_direction == "down":
            # left from current point of view
            if pred == -1:
                self.agent.body.change_direction("right")
            # right from current point of view
            elif pred == 1:
                self.agent.body.change_direction("left")


    def get_input_data(self, action):
        # all the prediction of the next frame's collision movements
        coll_pred = self.agent.body.self_collision_prediction()
        # get distance from the snake and food
        distance_from_food = self.agent.body.distance_from_food(self.food_stack[0])
        angle = self.get_angle()
        return np.array([coll_pred[0], coll_pred[1], coll_pred[2], angle, action])


    def train_agent(self):
        training_data = []
        high_score = 3
        for i in range(self.total_training_games):
            print("On game number: {}".format(i + 1))
            print("Highest score: {}".format(high_score))
            prev_score = 3
            prev_food_distance = self.agent.body.distance_from_food(self.food_stack[0])
            for j in range(self.goal_steps):
                end, nn_data = self.render_training_frame()
                if end:
                    training_data.append([nn_data, -1])
                    # when game ends we reconstruct the body of the snake
                    self.agent.create_new_body()
                    self.spawn_food()
                    break
                else:
                    food_distance = self.agent.body.distance_from_food(self.food_stack[0])
                    if self.agent.body.score > prev_score or food_distance < prev_food_distance:
                        training_data.append([nn_data, 1])
                        prev_score = self.agent.body.score
                        if prev_score > high_score:
                            high_score = prev_score
                    else:
                        training_data.append([nn_data, 0])
                    prev_food_distance = food_distance
            # end of each game a new body is created
            self.agent.create_new_body()
            self.spawn_food()
        self.agent.learn(training_data)

    def render_training_frame(self):
        pygame.event.pump()

        self.screen.fill(self.background_color)

        self.display_info()

        for food in self.food_stack:
            food.draw(self.screen)

        action = random.randint(0, 2) - 1

        nn_data = self.get_input_data(action)

        self.map_keys(action)

        end = self.agent.body.draw(self.screen, self.go_through_boundary)

        # check here if the snake ate the food
        if self.consumption_check():
            self.spawn_food()
            # finally we grow the snake as well by adding a new segment to the snake's body
            self.agent.body.grow()

        pygame.display.flip()

        return end, nn_data



    def game_loop(self, key_input = None):
        pygame.event.pump()

        self.screen.fill(self.background_color)

        self.display_info()

        for food in self.food_stack:
            food.draw(self.screen)

        predictions = []
        for action in range(-1, 2):
            predictions.append(self.agent.brain.predict(self.get_input_data(action).reshape(-1, 5, 1)))

        action = np.argmax(np.array(predictions)) - 1

        self.map_keys(action)

        end = self.agent.body.draw(self.screen, self.go_through_boundary)

        # check here if the snake ate the food
        if self.consumption_check():

            self.spawn_food()

            # finally we grow the snake as well by adding a new segment to the snake's body
            self.agent.body.grow()

        pygame.display.flip()

        return end
