from Player import Player
from Snake import Snake
import pygame
import random
from util import *

class SinglePlayer(Player):
    def __init__(self, screen, speed):
        super().__init__(screen)
        # takes in x, y of the snake and the speed of the snake
        self.snakes_speed = speed
        self.snake = Snake(50, 50, self.snakes_speed, WINDOW_SIZE[0], WINDOW_SIZE[0])
        self.go_through_boundary = False

    def consumption_check(self):
        if self.collision(self.snake, self.food_stack[0]):
            return True
        else:
            return False

    def self_collision_check(self):
        # THERE IS A BUG HERE PLS FIX THIS
        bodies = self.snake.get_body()

        seg_count = 0
        for segment in bodies:
            # we check for collision only if theres more than 2 head
            if seg_count > 2:
                if self.collision(self.snake, segment):
                    return True
            seg_count += 1
        # False is returend if and ONLY if we get out of the loop and have iterated over every single segment and found no collision
        # this prevents the check from just checking one segment finding no collision and returning
        return False

    def game_loop(self, key_input = None):
        pygame.event.pump()

        self.screen.fill(self.background_color)

        for food in self.food_stack:
            food.draw(self.screen)

        if not key_input:
            boundary_collision_check = self.snake.draw(self.screen, self.go_through_boundary)

        else:
            self.snake.change_direction(key_input)
            boundary_collision_check = self.snake.draw(self.screen, self.go_through_boundary)

        # check here if the snake ate the food
        if self.consumption_check():

            self.spawn_food()

            # finally we grow the snake as well by adding a new segment to the snake's body
            self.snake.grow()

        pygame.display.flip()

        return boundary_collision_check, self.self_collision_check()
