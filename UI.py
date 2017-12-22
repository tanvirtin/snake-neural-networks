from SnakeGame import SnakeGame
import time

class UI(object):
    def __init__(self):
        self.game = None

    def run(self):
        while True:
            pick = input("1. Brute force Reinforcement Algorithm\n2. Genetic Algorithm\n3. Quit\n-> ")
            # RL
            if int(pick) == 1:
                while True:
                    pick = input("Would you like a pre trained Neural Network (y/n): ")
                    if pick == "y":
                        self.game = SnakeGame(reinforcement_learning = True, use_keras = True, pre_trained = True)
                        self.game.game_loop()
                        # we are done return the function
                        return
                    elif pick == "n":
                        pick = input("1. Keras MLP\n2. Personal Implementation of MLP\n3. Quit\n-> ")
                        if int(pick) == 1:
                            while True:
                                pick = input("Enter the number of games you would like to train the snake for: ")
                                if not pick.isdigit():
                                    print("Input should be a number to proceed!")
                                else:
                                    self.game = SnakeGame(reinforcement_learning = True, use_keras = True, pre_trained = False)
                                    self.game.gather_data(int(pick))
                                    self.game.train_agent()
                                    self.game.game_loop()
                                    return
                        elif int(pick) == 2:
                            while True:
                                pick = input("Enter the number of games you would like to train the snake for: ")
                                if not pick.isdigit():
                                    print("Input should be a number to proceed!")
                                else:
                                    self.game = SnakeGame(reinforcement_learning = True, use_keras = False, pre_trained = False)
                                    self.game.gather_data(int(pick))
                                    self.game.train_agent()
                                    self.game.game_loop()
                                    return
                        elif int(pick) == 3:
                            return
                        else:
                            print("Please select one of the options above\n")
                    else:
                        print("Please type in either y or n")
            # GA
            elif int(pick) == 2:
                while True:
                    pick = input("Snakes per generation: ")
                    if not pick.isdigit():
                        print("Input must be a number!")
                    else:
                        self.game = SnakeGame(reinforcement_learning = False, population_size = int(pick))
                        while True:
                            pick = input("Number of generations: ")
                            if not pick.isdigit():
                                print("Input must be a number!")
                            else:
                                self.game.train_agent(int(pick))
                                self.game.game_loop()
                                return
            # Quit
            elif int(pick) == 3:
                return
            else:
                print("Please select from one of the options above\n")
