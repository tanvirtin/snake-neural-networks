from SnakeGame import SnakeGame
import time
import sys

def main():
    game = SnakeGame(True)

    game.prepare_players()

    game.game_loop()

if __name__ == "__main__":
    main()
