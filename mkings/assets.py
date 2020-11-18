import pygame
import os
from .constants import IMAGES_PATH

class Asset:
    image = {}
    
    def __init__(self):
        for filename in os.listdir(IMAGES_PATH):
            if filename.endswith(".png"):
                Asset.image[filename] = pygame.image.load(IMAGES_PATH + filename).convert_alpha()
