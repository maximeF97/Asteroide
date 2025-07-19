import random
import random
import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from assets import BACKGROUND_IMAGE
from power_up import BoostBar
from power_up import Extra_Life_power_up
from power_up import Shield_power_up
from power_up import TripleShot_power_up
from assets import SHIELD
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    score = SCORE
    boost_bar = BoostBar(x=260, y=20)  # Create the actual bar instance
    shield_power_up = Shield_power_up(x=300, y= 400)
    extra_life_power_up = Extra_Life_power_up(x=500, y= 400)
    tripleShot_power_up = TripleShot_power_up(x=700, y= 400)
    power_ups = [shield_power_up, extra_life_power_up, tripleShot_power_up]
    shield_spawn_timer = 0
    extra_life_power_up_spawn_timer = 0
    tripleShot_power_up_spawn_timer = 0
    next_shield_spawn = random.uniform(20, 35)
    next_extra_life_spawn = random.uniform(40, 50)
    next_triple_shot_spawn = random.uniform(60, 70)
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
    Shield_power_up.containers = (power_ups, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,boost_bar)

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
                if player.shield.active:
                    print("Shield active! No damage taken.")
                    continue
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
        for powerup in power_ups[:]:
            if player.collision(powerup):
                if isinstance(powerup, Extra_Life_power_up) and player.collision(powerup):
                    player_health += 1
                    power_ups.remove(powerup)
                elif isinstance(powerup, Shield_power_up) and not player.shield.active:
                    player.shield.activate()
                    power_ups.remove(powerup)  # Remove it from the game
                elif isinstance(powerup, TripleShot_power_up):
                    player.triple_shot_active = True
                    player.triple_shot_timer = player.triple_shot_duration
                    power_ups.remove(powerup)    
        screen.blit(BACKGROUND_IMAGE, (0, 0))

        font = pygame.font.SysFont("comicsans", 30, True)
        text = font.render("Health: " + str(player_health), 1, (255, 255, 255))  
        score_text = font.render("PLAYER_SCORE: " + str(score), 1, (255, 255, 255))   
        screen.blit(text, (390, 10))
        screen.blit(score_text, (10, 10))
        boost_bar.draw(screen)
        for powerup in power_ups:
            powerup.draw(screen)
        for obj in drawable:
            obj.draw(screen)
        

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000
        # Update shield power-up spawn timer
        shield_spawn_timer += dt
        if shield_spawn_timer >= next_shield_spawn:
            shield_spawn_timer = 0
            next_shield_spawn = random.uniform(10, 20)

            # Random position on screen (avoid edges)
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)

            shield_power_up = Shield_power_up(x, y)
            power_ups.append(shield_power_up)

        extra_life_power_up_spawn_timer += dt
        if extra_life_power_up_spawn_timer >= next_extra_life_spawn:
            extra_life_power_up_spawn_timer = 0
            next_extra_life_spawn = random.uniform(30, 45)  # Make extra life spawn slower

            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)

            new_life = Extra_Life_power_up(x, y)
            power_ups.append(new_life)     


if __name__ == "__main__":
    main()
