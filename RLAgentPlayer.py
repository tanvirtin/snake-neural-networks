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
from tqdm import tqdm
import time

class RLAgentPlayer(Player):
    def __init__(self, screen, speed):
        super().__init__(screen)
        # takes in x, y of the snake and the speed of the snake
        self.agent = RLAgent(speed, True)
        self.go_through_boundary = True
        # total number of games required to train
        self.total_training_games = 10
        # number of frames rendered to collect the data
        self.goal_steps = 2000
        self.frames = 0
        # try to load the numpy data, if not possible then set the training_data to an empty list
        try:
            print("Training data loaded from disk...")
            # loaded training_data needs to be converted into a list
            self.training_data = np.load("./rl-learning-data/rl-data.npy").tolist()
        except:
            print("Training data couldn't be loaded from disk...")
            self.training_data = []
        self.game_num = 0

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

        head_x = self.agent.body.get_x()
        head_y = self.agent.body.get_y()

        segment_x = self.agent.body.body[0].get_x()
        segment_y = self.agent.body.body[0].get_y()

        food_x = self.food_stack[0].get_x()
        food_y = self.food_stack[0].get_y()

        snake_direction = np.array([head_x, head_y]) - np.array([segment_x, segment_y])
        food_direction = np.array([food_x, food_y]) - np.array([head_x, head_y])

        a = snake_direction / np.linalg.norm(snake_direction)
        b = food_direction / np.linalg.norm(food_direction)

        return math.atan2(a[0] * b[1] - a[1] * b[0], a[0] * b[0] + a[1] * b[1]) / math.pi

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

    def get_input_data(self):
        # all the prediction of the next frame's collision movements
        coll_pred = self.agent.body.self_collision_prediction()
        # get distance from the snake and food
        distance_from_food = self.agent.body.distance_from_food(self.food_stack[0])
        angle = self.get_angle()
        return [coll_pred[0], coll_pred[1], coll_pred[2], angle]

    def train_agent(self):
        for _ in range(self.total_training_games):
            self.one_game_iteration()

        print("Training data saved to disk...")
        # save the numpy data
        np.save("./rl-learning-data/rl-data.npy", self.training_data)
        print("Begining to train with {} data".format(len(self.training_data)))
        self.agent.learn(self.training_data)

    def one_game_iteration(self):
        self.game_num += 1
        print("On game: {}".format(self.game_num))
        prev_score = 3
        prev_food_distance = self.agent.body.distance_from_food(self.food_stack[0])
        prev_nn_data = self.get_input_data()
        steps = 0
        for j in tqdm(range(self.goal_steps)):
            steps += 1
            end, curr_nn_data, current_action = self.render_training_frame()
            prev_nn_data.append(current_action)
            prev_nn_data = np.array(prev_nn_data)
            if end:
                self.training_data.append([prev_nn_data, -1])
                # when game ends we reconstruct the body of the snake
                self.agent.create_new_body()
                self.spawn_food()
                break
            else:
                food_distance = self.agent.body.distance_from_food(self.food_stack[0])
                if self.agent.body.score > prev_score or food_distance < prev_food_distance:
                    self.training_data.append([prev_nn_data, 1])
                else:
                    self.training_data.append([prev_nn_data, 0])
                prev_food_distance = food_distance
                prev_nn_data = curr_nn_data
                prev_score = self.agent.body.score
        # end of each game a new body is created
        self.agent.create_new_body()
        self.spawn_food()

    def process_training_data(self, right_direction, wrong_direction):
        new_training_data = []
        to_match = 0
        for i in range(len(self.training_data)):
            if self.training_data[i][1] == 1:
                to_match += 1
                if to_match != wrong_direction:
                    new_training_data.append(self.training_data[i])
            else:
                new_training_data.append(self.training_data[i])

        return new_training_data

    def render_training_frame(self):
        pygame.event.pump()

        for food in self.food_stack:
            food.draw(self.screen)

        action = random.randint(-1, 2)

        self.map_keys(action)

        end = self.agent.body.draw(self.screen, self.go_through_boundary)

        # check here if the snake ate the food
        if self.consumption_check():
            self.spawn_food()
            # finally we grow the snake as well by adding a new segment to the snake's body
            self.agent.body.grow()

        nn_data = self.get_input_data()

        return end, nn_data, action

    def kill_idle_game(self):
        self.frames += 1
        if self.frames == 400:
            self.frames = 0
            return True

    def use_brain_to_move(self):
        prev_nn_data = self.get_input_data()

        predictions = []
        for action in range(-1, 2):
            nn_data = self.get_input_data()
            nn_data.append(action)
            nn_data = np.array(nn_data)
            # depending on previous observation what move should i generate
            predictions.append(self.agent.predict(nn_data))

        action = np.argmax(np.array(predictions)) - 1

        self.map_keys(action)


    def game_loop(self, key_input = None):
        while True:
            pygame.event.pump()

            self.screen.fill(self.background_color)

            self.display_info()

            for food in self.food_stack:
                food.draw(self.screen)

            self.use_brain_to_move()

            end = self.agent.body.draw(self.screen, self.go_through_boundary)

            # #if snake doesnt do anything or the snake died then kill the game
            # if self.kill_idle_game() or end:
            #     return

            # check here if the snake ate the food
            if self.consumption_check():

                self.frames = 0

                self.spawn_food()

                # finally we grow the snake as well by adding a new segment to the snake's body
                self.agent.body.grow()

            pygame.display.flip()

            time.sleep(0.05)
