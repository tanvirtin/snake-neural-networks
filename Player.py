from Snake import Snake
from Food import Food
import pygame
import random
from util import *

class Player(object):
    def __init__(self, screen):
        self.screen = screen
        self.background_color = pygame.Color("white")
        self.weird_boundary_offset = 25
        self.food_stack = [Food(random.randint(self.weird_boundary_offset, WINDOW_SIZE[0] - self.weird_boundary_offset), random.randint(self.weird_boundary_offset, WINDOW_SIZE[0] - self.weird_boundary_offset))]

    # def get_game_pixels(self):
    #     # get the game pixel
    #     pixels = pygame.surfarray.array3d(pygame.display.get_surface())
    #     # # convert pixel into greyscale image with only 1 channel
    #     # cv2 is far more superior then any other library in image manipulation
    #     pixels = cv2.cvtColor(pixels, cv2.COLOR_BGR2GRAY) / 255
    #
    #     return pixels

    def spawn_food(self):
        # we pop the food from the stack
        self.food_stack.pop()
        # and push another food at another random location
        self.food_stack.append(Food(random.randint(self.weird_boundary_offset, WINDOW_SIZE[0] - self.weird_boundary_offset), random.randint(self.weird_boundary_offset, WINDOW_SIZE[0] - self.weird_boundary_offset)))
