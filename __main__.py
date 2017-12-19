from SnakeGame import SnakeGame
import time
import sys

def main():
    game = SnakeGame()

    game.prepare_players()

    while True:
        end = game.game_loop()
        #time.sleep(0.05)


if __name__ == "__main__":
    main()
