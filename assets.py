import pygame
import os
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = os.path.dirname(__file__)

    return os.path.join(base_path, relative_path)

BACKGROUND_IMAGE = pygame.image.load(resource_path("assets/galaxy-night-view.jpg"))
