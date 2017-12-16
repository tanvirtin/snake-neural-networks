from GameObj import GameObj
import pygame

# I will keep a stack in the main game object which will get popped
# when the snake eats the apple

class Food(GameObj):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20)
        self.food_img = pygame.transform.scale(pygame.image.load("./assets/food.png"), (self.dimensions[0], self.dimensions[0]))

    def get_coor(self):
        return self.coordinates

    def get_size(self):
        return self.dimensions[0]

    def draw(self, screen):
        screen.blit(self.food_img, (self.coordinates[0], self.coordinates[1]))
