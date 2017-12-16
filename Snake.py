from SnakeSegment import SnakeSegment
import pygame

# Snake is a SnakeSegment itself and also contains other SnakeSegments
class Snake(SnakeSegment):
    def __init__(self, x, y, speed, boundary_x, boundary_y):
            super().__init__(x, y, speed, boundary_x, boundary_y, head = True)
            self.head_size = 20
            # contains the segments which make up the body
            self.body = []
            self.reward = 0
            # the image of the head is stored here
            # I need to scale the image to correct size
            self.head = pygame.transform.scale(pygame.image.load("./assets/head.png"), (self.head_size, self.head_size))

    def get_body(self):
        return self.body

    def grow(self):
        # NOTE the x and y value of the SnakeSegment doesn't matter atm as it gets updated when it gets drawn
        self.body.append(SnakeSegment(0, 0, self.speed, self.boundary_x, self.boundary_y, False))
        self.reward += 1

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

        # in pygame the y coordinates start at the maximum value or in other words it is flipped
        if self.current_direction == "up":
            # up direction
            self.coordinates[1] -= self.speed

        elif self.current_direction == "down":
            # down direction
            self.coordinates[1] += self.speed

        elif self.current_direction == "right":
            # down direction
            self.coordinates[0] += self.speed

        elif self.current_direction == "left":
            # down direction
            self.coordinates[0] -= self.speed

        # if go through_boundary is specified then the snake goes through the boundary
        if go_through_boundary:
            self.boundary_check_through()
        else:
            boundary_collision = self.boundary_collision()

    #    pygame.draw.rect(screen, self.color, pygame.Rect(self.coordinates[0], self.coordinates[1], self.dimensions[0], self.dimensions[1]))

        screen.blit(self.head, (self.coordinates[0], self.coordinates[1]))

        self.update_body(screen, prev_x, prev_y, previous_direction, go_through_boundary)

        return boundary_collision
