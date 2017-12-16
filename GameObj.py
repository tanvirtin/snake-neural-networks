import pygame

class GameObj(object):
    # the game object takes the coordinates, the dimensions and the color as its initialization parameters
    def __init__(self, x, y, w, h):
        # coordinates is the x and y value at which the object will be drawn in pygame
        self.coordinates = [x, y]
        # dimension is the height and width of the object
        self.dimensions = [w, h]

    def get_x(self):
        return self.coordinates[0]

    def get_y(self):
        return self.coordinates[1]

    def get_size(self):
        return self.dimensions[0]
