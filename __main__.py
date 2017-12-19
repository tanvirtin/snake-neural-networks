from SnakeGame import SnakeGame
import time
import sys

def main():
    game = SnakeGame()

    game.prepare_players()

    while True:
        end = game.game_loop()
        #time.sleep(0.05)

    # while not keyboard.is_pressed("q"):
    #     # if keyboard.is_pressed("up"):
    #     #     end = game.sp_game_loop("up")
    #     # elif  keyboard.is_pressed("down"):
    #     #     end = game.sp_game_loop("down")
    #     # elif  keyboard.is_pressed("left"):
    #     #     end = game.sp_game_loop("left")
    #     # elif  keyboard.is_pressed("right"):
    #     #     end = game.sp_game_loop("right")
    #     #
    #     # if keyboard.is_pressed("j"):
    #     #     end = game.sp_game_loop(-1)
    #     # elif  keyboard.is_pressed("k"):
    #     #     end = game.sp_game_loop(1)
    #     # elif  keyboard.is_pressed("i"):
    #     #     end = game.sp_game_loop(0)
    #

if __name__ == "__main__":
    main()
