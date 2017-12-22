from SnakeGame import SnakeGame
import time

class Test(object):
    def __init__(self):
        self.game = None

    def run(self):
        self.game = SnakeGame(reinforcement_learning = False, population_size = 10)
        self.game.train_agent(30)
        self.game.test_agent(100)
        #self.game.game_loop()
