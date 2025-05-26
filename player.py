import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot
from asteroid import Asteroid
from power_up import BoostBar
from power_up import Shield
from power_up import Shield_power_up

class Player(CircleShape):
    def __init__(self, x, y , boost_bar,):
        self.shield = Shield(x,y)
        self.boost_bar = BoostBar(x, y)
        self.boost_bar.current_value = 100  # Initialize the boost bar to full
        super().__init__(x, y, PLAYER_RADIUS)
        self.original_image = pygame.image.load("assets/new_p.png").convert_alpha()
        self.images = {
            "boost": pygame.image.load("assets/fire_boost.png").convert_alpha(),
            "ship": self.original_image
        }

        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.rotation = 0
        self.shoot_timer = 0
        self.visible = True
        self.flash_timer = 0
        self.is_boosting = False

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        self.shoot_timer -= dt
        keys = pygame.key.get_pressed()

        self.is_boosting = False

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
        if keys[pygame.K_b] and self.boost_bar.current_value > 0:
            self.boost_bar.update(-40 * dt)
            self.move(dt * 2)
            self.is_boosting = True
        else:
            
            self.boost_bar.update(10 * dt)
            self.is_boosting = False
        # Rotate and update rect
        self.image = pygame.transform.rotate(self.original_image, -self.rotation)
        self.rect = self.image.get_rect(center=self.position)
        self.shield.update(dt)
        self.shield.position = self.position
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def draw(self, screen):
        if self.is_boosting:
            # Rotation de la flamme
            rotated_flame = pygame.transform.rotate(self.images["boost"], -self.rotation)

            # Calcul de la position juste derrière le vaisseau
            offset = pygame.Vector2(0, 55).rotate(self.rotation)  # Ajuste 35 si nécessaire
            flame_pos = self.position - offset

            # Obtenir le rectangle tourné pour le centrer
            flame_rect = rotated_flame.get_rect(center=flame_pos)

            # Dessiner la flamme derrière
            screen.blit(rotated_flame, flame_rect.topleft)
           


        # Dessiner le vaisseau au-dessus de la flamme
        self.shield.draw(screen)
        if self.visible:
            screen.blit(self.image, self.rect.topleft)

            

            