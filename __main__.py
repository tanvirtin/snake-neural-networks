import keyboard
from SnakeGame import SnakeGame
import time

def main():
    game = SnakeGame(True)

    while not keyboard.is_pressed("q"):
        if keyboard.is_pressed("w"):
            game.rl_game_loop("up")
        elif keyboard.is_pressed("s"):
            game.rl_game_loop("down")
        elif keyboard.is_pressed("a"):
            game.rl_game_loop("left")
        elif keyboard.is_pressed("d"):
            game.rl_game_loop("right")
        else:
            game.rl_game_loop()
        time.sleep(0.05)

if __name__ == "__main__":
    main()
