import pygame
from constants import *
# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
    def collision(self, other):
        if self.position.distance_to(other.position) < self.radius + other.radius:
            return True
   
    def draw(self, screen):
        pass


    def update(self, dt):
        pass