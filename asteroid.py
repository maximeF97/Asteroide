import pygame
from circleshape import CircleShape
from constants import *
import random

class Asteroid(CircleShape):
    asteroid_images = []
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        if not Asteroid.asteroid_images:
                Asteroid.asteroid_images = [
                    pygame.image.load("assets/aste1.png").convert_alpha(),
                    pygame.image.load("assets/ast_2.png").convert_alpha(),
                    pygame.image.load("assets/ast_3.png").convert_alpha()
                ]

        self.original_image = random.choice(Asteroid.asteroid_images)
        self.image = pygame.transform.scale(self.original_image, (int(radius * 2), int(radius * 2)))
        self.rect = self.image.get_rect(center=(x, y))
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = self.position
        self.warp_position()
    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        
        angle = random.uniform(20,50)
        a = self.velocity.rotate(angle)
        b = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = a * 1.2
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = b * 1.2
    def warp_position(self):
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

        self.rect.center = self.position
