import keyboard
from SnakeGame import SnakeGame
import time

def main():
    game = SnakeGame()

    while not keyboard.is_pressed("q"):
        game.ap_game_loop()
        time.sleep(0.05)

if __name__ == "__main__":
    main()
