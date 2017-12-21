from SnakeGame import SnakeGame
import time
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--genetic", help = "To use genetic algorithm implementation", action = "store_true")
    parser.add_argument("-rk", "--reinforcement_k", help = "To use brute force reinforcement algorithm implementation, using keras", action = "store_true")
    parser.add_argument("-ro", "--reinforcement_o", help = "To use brute force reinforcement algorithm implementation, our own implementation of multi layer perceptron", action = "store_true")
    args = parser.parse_args()

    if args.genetic:
        print("Snake is using genetic algorithm!")
        game = SnakeGame()

    elif args.reinforcement_k:
        print("Snake is using brute forced reinforcement algorithm using keras MLP!")
        game = SnakeGame(True, True)

    elif args.reinforcement_o:
        print("Snake is using brute forced reinforcement algorithm using our own implementation of MLP!")
        game = SnakeGame(True, False)

    game.gather_data()

    game.train_agent()

    game.game_loop()

if __name__ == "__main__":
    main()
