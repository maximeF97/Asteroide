import pygame
from assets import SHIELD
from circleshape import CircleShape
class Shield:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.radius = 30
        self.active = False
        self.duration = 5.0  # Shield lasts for 5 seconds
        self.timer = 0.0

    def activate(self):
        self.active = True
        self.timer = self.duration

    def update(self, dt):
        if self.active:
            self.timer -= dt
            if self.timer <= 0:
                self.active = False

    def draw(self, screen):
        if self.active:
            pygame.draw.circle(screen, "blue", (int(self.position.x), int(self.position.y)), self.radius, 2)

class Shield_power_up(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, 20)
        self.image = pygame.image.load("assets/shild_p_up.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
        self.rect = self.image.get_rect(center=(x, y))
        self.lifetime = 10
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        
class BoostBar:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.width = 100
        self.height = 10
        self.current_value = 0
        self.max_value = 100

    def update(self, value):
        
        self.current_value = max(0, min(self.current_value + value, self.max_value))


    def draw(self, screen):
        pygame.draw.rect(screen, "black", (self.position.x, self.position.y, self.width, self.height))
        fill_width = (self.current_value / self.max_value) * self.width
        pygame.draw.rect(screen, "green", (self.position.x, self.position.y, fill_width, self.height))