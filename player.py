import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot
from asteroid import Asteroid

class Player(CircleShape):
    def __init__(self, x, y,):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.visible = True
        self.flash_timer = 0
    def rotate(self,dt):
        self.rotation = self.rotation + (PLAYER_TURN_SPEED * dt)
    def draw(self,screen):
        if self.visible:
            pygame.draw.polygon(screen, "white", self.triangle(), 2)
    def update(self, dt):
        self.shoot_timer -= dt
        keys = pygame.key.get_pressed()
        if not self.visible:
            self.flash_timer -= dt
            if self.flash_timer <= 0:
                self.visible = True
                self.flash_timer = 0.1
                
        if keys[pygame.K_q]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_z]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shot()

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED 
    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    
        

        