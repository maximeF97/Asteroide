import pygame
import os
from constants import *
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = os.path.dirname(__file__)

    return os.path.join(base_path, relative_path)

BACKGROUND_IMAGE = pygame.image.load(resource_path("assets/aste_font1.png"))
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
PLAYER_IMAGE = pygame.image.load(resource_path("assets/new_p.png"))
ASTEROIDE_1_IMAGE = pygame.image.load(resource_path("assets/aste1.png"))
ASTEROIDE_2_IMAGE = pygame.image.load(resource_path("assets/ast_2.png"))
ASTEROIDE_3_IMAGE = pygame.image.load(resource_path("assets/ast_3.png"))

BOOST = pygame.image.load(resource_path("assets/fire_boost.png")),
SHIELD = pygame.image.load(resource_path("assets/shild_p_up.png")),
EXTRA_LIFE =pygame.image.load(resource_path("assets/life-p_up.png"))
TRIPLE_SHOT = pygame.image.load(resource_path("/home/fuhrm/boot.dev.ls/github.com/maximeF97/Asteroide/assets/asteroid pick.png"))
LASER = pygame.image.load(resource_path("assets/laser.png"))
BLAST = pygame.image.load(resource_path("assets/blast.png"))

