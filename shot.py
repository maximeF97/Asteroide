import pygame
import math
from constants import *
from circleshape import CircleShape
from assets import BLAST

class Shot(CircleShape):
    def __init__(self, x, y,angle = 0):
        super().__init__(x, y, SHOT_RADIUS)
        self.image = pygame.transform.scale(BLAST, (SHOT_RADIUS * 2, SHOT_RADIUS * 2))
        self.rect = self.image.get_rect(center=(x, y))

        speed = 500  # Try increasing from 50 to something faster
        direction = pygame.Vector2(0, 1).rotate(angle)  # ✅ now follows ship direction
        self.velocity = direction * speed

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        self.rect.center = self.position

    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = self.position

        if (self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or
                self.rect.right < 0 or self.rect.left > SCREEN_WIDTH):
            self.kill()


#  Triple shot function
def fire_triple_shot(x, y, base_angle, shot_group):
    angles = [base_angle, base_angle - 15, base_angle + 15]
    for angle in angles:
        shot = Shot(x, y, angle)
        shot_group.add(shot)
