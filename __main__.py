import keyboard
from SnakeGame import SnakeGame
import time
import sys

def main():
    game = SnakeGame(True)

    game.prepare_rl_player()

    while not keyboard.is_pressed("q"):
        end = game.rl_game_loop()
        time.sleep(0.05)


if __name__ == "__main__":
    main()
