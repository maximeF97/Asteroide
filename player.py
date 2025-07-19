import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot, fire_triple_shot
from power_up import BoostBar, Shield

class Player(CircleShape):
    def __init__(self, x, y, boost_bar):
        super().__init__(x, y, PLAYER_RADIUS)
        self.original_image = pygame.image.load("assets/new_p.png").convert_alpha()
        self.images = {
            "boost": pygame.image.load("assets/fire_boost.png").convert_alpha(),
            "ship": self.original_image
        }

        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.position = pygame.Vector2(x, y)
        self.rotation = 0
        self.shoot_timer = 0
        self.visible = True
        self.flash_timer = 0
        self.is_boosting = False

        self.shield = Shield(x, y)
        self.triple_shot_active = False
        self.triple_shot_timer = 0.0
        self.triple_shot_duration = 5.0
        self.boost_bar = boost_bar
        self.boost_bar.current_value = 100  # Start full

    def update(self, dt):
        self.shoot_timer -= dt
        keys = pygame.key.get_pressed()

        if self.triple_shot_active:
            self.triple_shot_timer -= dt
            if self.triple_shot_timer <= 0:
                self.triple_shot_active = False

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
            self.shot(Shot)
        if keys[pygame.K_b] and self.boost_bar.current_value > 0:
            self.boost_bar.update(-40 * dt)
            self.move(dt * 2)
            self.is_boosting = True
        else:
            self.boost_bar.update(10 * dt)
            self.is_boosting = False

        self.image = pygame.transform.rotate(self.original_image, -self.rotation)
        self.rect = self.image.get_rect(center=self.position)
        self.shield.update(dt)
        self.shield.position = self.position
        self.warp_position()

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shot(self, shot_group=None):
        if self.shoot_timer > 0:
            return

        self.shoot_timer = PLAYER_SHOOT_COOLDOWN

        if self.triple_shot_active:
            fire_triple_shot(self.position.x, self.position.y, self.rotation, shot_group)
        else:
            shot = Shot(self.position.x, self.position.y, self.rotation)
            shot_group.add(shot)

    def draw(self, screen):
        if self.is_boosting:
            rotated_flame = pygame.transform.rotate(self.images["boost"], -self.rotation)
            offset = pygame.Vector2(0, 55).rotate(self.rotation)
            flame_pos = self.position - offset
            flame_rect = rotated_flame.get_rect(center=flame_pos)
            screen.blit(rotated_flame, flame_rect.topleft)

        self.shield.draw(screen)
        if self.visible:
            screen.blit(self.image, self.rect.topleft)

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
