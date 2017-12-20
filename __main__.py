from SnakeGame import SnakeGame
import time
import sys

def main():
    game = SnakeGame(True)

    game.gather_data()

    #game.train_agent()

    # game.game_loop()

if __name__ == "__main__":
    main()
