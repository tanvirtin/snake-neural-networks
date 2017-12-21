from Player import Player
from Snake import Snake
import pygame
import random
from util import *
from collision_checker import *
from RLAgent import RLAgent
import numpy as np
import math
from tqdm import tqdm
import time

class RLAgentPlayer(Player):
    def __init__(self, screen, speed, use_keras = True, pre_trained = True, total_training_games = TOTAL_TRAINING_GAMES):
        super().__init__(screen)
        self.total_training_games = total_training_games
        # takes in x, y of the snake and the speed of the snake
        self.agent = RLAgent(speed, use_keras, pre_trained)
        self.go_through_boundary = True
        # total number of games required to train
        self.idle_frames = 0
        self.total_steps = 0
        # try to load the numpy data, if not possible then set the training_data to an empty list
        try:
            # loaded training_data needs to be converted into a list
            self.training_data = np.load("./rl-learning-data/rl-data.npy").tolist()
            print("Training data loaded from disk...")
        except:
            print("Training data couldn't be loaded from disk...")
            self.training_data = []
    def consumption_check(self):
        if collision(self.agent.body, self.food_stack[0]):
            return True
        else:
            return False

    def display_info(self, score, high_score):
        pygame.font.init()

        default_font = pygame.font.get_default_font()
        font_renderer = pygame.font.Font(default_font, 10)

        # To create a surface containing `Some Text`
        label = font_renderer.render("Score - {}, High score - {}".format(score, high_score), 1, (0,0,0)) # RGB Color
        self.screen.blit(label, (0,0))

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

    def gather_training_data(self):
        self.wrong_turn = 0
        self.wrong_direction = 0
        self.right_direction = 0

        for _ in tqdm(range(self.total_training_games)):
            self.one_game_iteration()

        print("Training data saved to disk...")
        # save the numpy data
        np.save("./rl-learning-data/rl-data.npy", self.training_data)

        average_steps = self.total_steps / self.total_training_games

        print("Total Number of right directions: {}".format(self.right_direction))
        print("Total Number of wrong directions: {}".format(self.wrong_direction))
        print("Total Number of wrong turns: {}".format(self.wrong_turn))
        print("Average frames rendered per game: {}".format(average_steps))


    def train_agent(self):
        print("Begining to train with {} data".format(len(self.training_data)))
        self.agent.learn(self.training_data)

    def one_game_iteration(self):
        score = 3
        prev_food_distance = self.agent.body.distance_from_food(self.food_stack[0])
        prev_nn_data = self.get_input_data()
        # end dictates if the game has finished or not, initially it will be false
        end = False
        # the game is played until it is ended, so till the snake either hits the wall or collides with itself
        while not end:
            self.total_steps += 1
            end, curr_nn_data, current_action = self.render_training_frame()
            prev_nn_data.append(current_action)
            prev_nn_data = np.array(prev_nn_data)
            if end:
                self.wrong_turn += 1
                self.training_data.append([prev_nn_data, -1])
                # when game ends we reconstruct the body of the snake
                self.agent.create_new_body()
                self.spawn_food()
                break
            else:
                food_distance = self.agent.body.distance_from_food(self.food_stack[0])
                if self.agent.body.score > score or food_distance < prev_food_distance:
                    self.right_direction += 1
                    self.training_data.append([prev_nn_data, 1])
                else:
                    self.wrong_direction += 1
                    self.training_data.append([prev_nn_data, 0])
                prev_food_distance = food_distance
                prev_nn_data = curr_nn_data
                score = self.agent.body.score
        # make end to what its initial state was
        end = False
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
        self.idle_frames += 1
        if self.idle_frames == 400:
            self.idle_frames = 0
            return True

    def use_brain_to_move(self):
        prev_nn_data = self.get_input_data()

        predictions = []
        # all three possible directions are generated and for all possible direction values given those inputs
        # we ask the neural network which direction to step to for positive effect
        for action in range(-1, 2):
            nn_data = self.get_input_data()
            nn_data.append(action)
            nn_data = np.array(nn_data)
            # depending on previous observation what move should i generate
            predictions.append(self.agent.predict(nn_data))

        action = np.argmax(np.array(predictions))

        # to map the range value
        action -= 1

        self.map_keys(action)

    def test_agent(self, dataset_games):
        game_iterations = 100
        total_score = 0
        high_score = 0

        max_step = 1000

        for _ in tqdm(range(game_iterations)):
            step = 0
            while True:
                step += 1
                score = self.agent.body.score

                for food in self.food_stack:
                    food.draw(self.screen)

                self.use_brain_to_move()

                end = self.agent.body.draw(self.screen, self.go_through_boundary)

                # when the snake dies and the game ends
                if end or step == max_step:
                    if score > high_score:
                        high_score = score

                    total_score += score
                    # break the loop when the game ends
                    self.agent.create_new_body()
                    break

                # check here if the snake ate the food
                if self.consumption_check():
                    self.idle_frames = 0
                    self.spawn_food()
                    # finally we grow the snake as well by adding a new segment to the snake's body
                    self.agent.body.grow()

        average_score = total_score / game_iterations

        data_prints = ["Neural Network played {}\n".format(dataset_games), "Highest Score in {} games: {}\n".format(game_iterations, high_score), "Average Score in {} games: {}\n".format(game_iterations, average_score)]

        with open("test-result.txt", "a") as myfile:
            for prints in data_prints:
                myfile.write(prints)
                print(prints)


    def game_loop(self):
        game_iterations = 5
        high_score = 0

        for _ in range(game_iterations):
            while True:
                pygame.event.pump()

                self.screen.fill(self.background_color)

                score = self.agent.body.score
                self.display_info(score, high_score)

                for food in self.food_stack:
                    food.draw(self.screen)

                self.use_brain_to_move()

                end = self.agent.body.draw(self.screen, self.go_through_boundary)

                #if snake doesnt do anything or the snake died then kill the game
                if end:
                    # when the snake dies
                    print("Died after turning its head -> {}".format(self.agent.body.current_direction))
                    time.sleep(1)
                    if score > high_score:
                        high_score = score
                    # break the loop when the game ends
                    self.agent.create_new_body()
                    break

                # check here if the snake ate the food
                if self.consumption_check():
                    self.idle_frames = 0
                    self.spawn_food()
                    # finally we grow the snake as well by adding a new segment to the snake's body
                    self.agent.body.grow()

                pygame.display.flip()

                time.sleep(0.05)

        print("High score -> {}".format(high_score))
