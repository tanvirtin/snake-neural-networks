import pygame
from GameObj import GameObj
import random

class SnakeSegment(GameObj):
    def __init__(self, x, y, speed, boundary_x, boundary_y, head = False, default_direction = "up"):
        self.body_size = 20
        super().__init__(x, y, self.body_size, self.body_size)
        self.weird_boundary_offset = 19
        if not head:
            # the image of the body is stored here
            # I need to scale the image to correct size
            self.body = pygame.transform.scale(pygame.image.load("./assets/body.png"), (self.body_size, self.body_size))
        self.boundary_x = boundary_x
        self.boundary_y = boundary_y
        self.speed = speed
        self.current_direction = default_direction
        self.previous_direction = self.current_direction

    def change_direction(self, direction):
        # we go down if and only if our current direction is not up, so we can go down if
        # we are already down, left or right
        if direction == "down" and self.current_direction == "up":
            return
        # similarly if we are
        if direction == "up" and self.current_direction == "down":
            return
        # similarly if you are going left you cant go right
        if direction == "left" and self.current_direction == "right":
            return
        # if you are going right you cant go left
        if direction == "right" and self.current_direction == "left":
            return
        # I change the previous_direction to to what current_direction is
        self.previous_direction = self.current_direction
        # then I change the current_direction itself to the new direction provided
        self.current_direction = direction


    # draws the segment, go_through by default is false
    def draw(self, screen, x, y, go_through = False):

        # the previous coordinates will be stored in variables and returned, for the segment before the values gets
        # updated to get redrawn
        prev_x = self.coordinates[0]
        prev_y = self.coordinates[1]
        prev_direction = self.previous_direction

        # change the coordinates of the segment to the coordinates of the x and y provided
        self.coordinates[0] = x
        self.coordinates[1] = y

        # the segments go through the wall if specified
        if go_through:
            self.boundary_check_through()

        screen.blit(self.body, (self.coordinates[0], self.coordinates[1]))

        return prev_x, prev_y, prev_direction

    # checks the boundary for the segment
    # goes through the boundary and comes through the other end
    def boundary_check_through(self):
        # y boundary check if we go too up
        if self.coordinates[1] < 0:
            self.coordinates[1] = self.boundary_y

        # y boundary check if we go too down
        elif self.coordinates[1] > self.boundary_y:
            self.coordinates[1] = 0

        # x boundary check if we go too right
        elif self.coordinates[0] > self.boundary_x:
            self.coordinates[0] = 0

        # x boundary check we go too left
        elif self.coordinates[0] < 0:
            self.coordinates[0] = self.boundary_x

    def boundary_collision(self, snake):
        if snake.coordinates[1] < 0 or snake.coordinates[1] > snake.boundary_y - snake.weird_boundary_offset or snake.coordinates[0] > snake.boundary_x - snake.weird_boundary_offset or snake.coordinates[0] < 0:
            return True
        return False
