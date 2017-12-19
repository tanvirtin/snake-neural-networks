from SnakeSegment import SnakeSegment
import pygame
import math
from collision_checker import *
import copy
import numpy as np

# Snake is a SnakeSegment itself and also contains other SnakeSegments
class Snake(SnakeSegment):
    def __init__(self, x, y, speed, boundary_x, boundary_y):
        super().__init__(x, y, speed, boundary_x, boundary_y, head = True)
        self.head_size = 20
        # contains the segments which make up the body
        self.body = []
        # the image of the head is stored here
        # I need to scale the image to correct size
        self.head = pygame.transform.scale(pygame.image.load("./assets/head.png"), (self.head_size, self.head_size))
        self.score = 0

    def self_collision_check(self, snake):
        bodies = snake.body
        seg_count = 0
        for segment in bodies:
            # we check for collision only if theres more than 2 head
            if seg_count > 2:
                if snake_collision(snake, segment):
                    return True
            seg_count += 1
        # False is returend if and ONLY if we get out of the loop and have iterated over every single segment and found no collision
        # this prevents the check from just checking one segment finding no collision and returning
        return False

    # takes a snake object and moves it in the direction the snake object is facing
    def move_snake_in_its_direction(self, snake):
        # in pygame the y coordinates start at the maximum value or in other words it is flipped
        if snake.current_direction == "up":
            # up direction
            snake.coordinates[1] -= snake.speed

        elif snake.current_direction == "down":
            # down direction
            snake.coordinates[1] += snake.speed

        elif snake.current_direction == "right":
            # down direction
            snake.coordinates[0] += snake.speed

        elif snake.current_direction == "left":
            # down direction
            snake.coordinates[0] -= snake.speed

        return snake

    def self_collision_prediction_helper(self, direction):
        # a deep copy of self needs to be made to prevent pointer to self and changing self's attributes
        snake_clone = copy.deepcopy(self)
        # the direciton is changed
        snake_clone.change_direction(direction)
        # new x and y coordinate of the snake is obtained
        snake_clone = self.move_snake_in_its_direction(snake_clone)

        pred_1 = self.self_collision_check(snake_clone)
        pred_2 = self.boundary_collision(snake_clone)

        if pred_1 or pred_2:
            return 1
        return 0

    # this function will determine if you turn turn left, right or stay in your current direction
    # will you collide with your self or not
    def self_collision_prediction(self):
        left_collision = None
        front_collision = None
        right_collision = None


        if self.current_direction == "up":
            # if you are going up you can either continue to go up
            # you can go left and you can go right

            # If you take a left turn from your point of view what happens
            # check left
            left_collision = self.self_collision_prediction_helper("left")

            # If you take a right turn from your point of view what happens
            # check right
            right_collision = self.self_collision_prediction_helper("right")

            # If you keep going up what happens
            # check up
            front_collision = self.self_collision_prediction_helper("up")


        elif self.current_direction == "down":
            # if you are going down you can either continue to go down
            # you can go left and you can go right

            # if you take a left turn from your point of view what happens
            # check right
            left_collision = self.self_collision_prediction_helper("right")

            # if you take a right turn from your point of view what happens
            # check left
            right_collision = self.self_collision_prediction_helper("left")

            # if you keep going your current direction what happens
            # go down
            front_collision = self.self_collision_prediction_helper("down")


        elif self.current_direction == "left":
            # if you are going left you can either continue to go left
            # you can go up and you can go down

            # if you take a left turn from your point of view what happens
            # check down
            left_collision = self.self_collision_prediction_helper("down")

            # if you take a right turn from your point of view what happens
            # check up
            right_collision = self.self_collision_prediction_helper("up")

            # if you keep going your current direction what happens
            # check left
            front_collision = self.self_collision_prediction_helper("left")


        elif self.current_direction == "right":
            # if you are going right you can either continue to go right
            # you can go up and you can go down

            # if you take a left turn from your point of view what happens
            # check up
            left_collision = self.self_collision_prediction_helper("up")

            # if you take a right turn from your point of view what happens
            # check down
            right_collision = self.self_collision_prediction_helper("down")

            # if you keep going your current direction what happens
            # check right
            front_collision = self.self_collision_prediction_helper("right")

        return left_collision, front_collision, right_collision

    def get_body(self):
        return self.body

    def snake_length(self):
        return 1 + len(self.body)

    def distance_from_food(self, food):
        x_distance = self.distance_from_food_x(food)
        y_distance = self.distance_from_food_y(food)

        #math.sqrt(x_distance**2 + y_distance**2) - food.get_size()

        return np.linalg.norm(np.array([x_distance, y_distance]))

    def distance_from_food_x(self, food):
        return self.coordinates[0] - food.get_coor()[0]

    def distance_from_food_y(self, food):
        return self.coordinates[1] - food.get_coor()[1]

    def get_head_coor(self):
        return self.coordinates

    def get_tail_coor(self):
        return self.body[-1].coordinates

    def get_mid_coor(self):
        midpoint = (len(self.body) / 2)
        midpoint = int(midpoint)
        #print("Body has length: {}, midpoint is: {}".format(len(self.body), midpoint))
        return self.body[midpoint].coordinates

    def grow(self):
        # NOTE the x and y value of the SnakeSegment doesn't matter atm as it gets updated when it gets drawn
        self.body.append(SnakeSegment(0, 0, self.speed, self.boundary_x, self.boundary_y, False))
        self.score += 1

    # MAIN GAME LOGIC TO UPDATE THE BODIES
    # this function will be invoked and the head's previous x and y coordinates
    # before it is about to be redrawn again in the current game loop will be passed in
    def update_body(self, screen, prev_x, prev_y, previous_direction, go_through):
        # each segment in the body will return its previous x and y coordinates before it gets updated
        for segment in self.body:
            segment.change_direction(previous_direction)
            # each segment basically gets updated by the previous x and y coordinates of its previous segment (if we are dealing
            # with the 0th index in the segment array then the 0th index will get the previous value of the head segment), the x and y coordinate
            # is the previous segments x and y coordinates before it gets redrawn, kind of tricky to understand
            # so when in the next frame all the segment will be at the position of their previous segment's position, this creates the snake
            # body delay effect
            prev_x, prev_y, previous_direction = segment.draw(screen, prev_x, prev_y, go_through)


    # draws the segment
    def draw(self, screen, go_through_boundary = False):
        # by default boundary_check is always true, depending on the if we are checking if collision
        # occurs in the boundary we assign this variable
        boundary_collision = False

        # previous x and y coordinates to be passed on to the segments
        prev_x = self.coordinates[0]
        prev_y = self.coordinates[1]
        previous_direction = self.previous_direction

        self = self.move_snake_in_its_direction(self)

        # if go through_boundary is specified then the snake goes through the boundary
        if go_through_boundary:
            self.boundary_check_through()
        else:
            boundary_collision = self.boundary_collision(self)

        screen.blit(self.head, (self.coordinates[0], self.coordinates[1]))

        self.update_body(screen, prev_x, prev_y, previous_direction, go_through_boundary)

        if self.self_collision_check(self) or boundary_collision:
            return True

        return False
