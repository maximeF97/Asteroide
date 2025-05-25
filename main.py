
import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from assets import BACKGROUND_IMAGE
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    score = SCORE
    
    clock = pygame.time.Clock()
    player_health = 3
    invincible = False
    invincibility_timer = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()
    Shot.containers = (shots, updatable, drawable)
    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)
        if invincible:
            invincibility_timer -= dt
            if invincibility_timer <= 0:
                invincible = False
        for asteroid in asteroids:        
            if not invincible and asteroid.collision(player):
                player_health -= 1
                print(f"Player hit!! health{player_health}")
                invincible = True
                invincibility_timer = 1.0
                player.visible = False
                player.flash_timer = 0.1
                if player_health <= 0:
                    print("Game over!")
                    pygame.quit()
                    sys.exit()

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collision(shot):
                    score += 1
                    asteroid.split()
                    shot.kill()
                    
        screen.blit(BACKGROUND_IMAGE, (0, 0))

        font = pygame.font.SysFont("comicsans", 30, True)
        text = font.render("Health: " + str(player_health), 1, (255, 255, 255))  
        score_text = font.render("PLAYER_SCORE: " + str(score), 1, (255, 255, 255))   
        screen.blit(text, (390, 10))
        screen.blit(score_text, (10, 10))
        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
