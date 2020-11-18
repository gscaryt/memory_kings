import pygame
import os
import time
from .constants import IMAGES_PATH

class Asset:
    image = {}
    
    def __init__(self):
        start=time.time()
        for i, filename in enumerate(os.listdir(IMAGES_PATH)):
            if filename.endswith(".png"):
                Asset.image[filename] = pygame.image.load(IMAGES_PATH + filename).convert_alpha()
                print(f"Loading Assets: {i+1}/{len(os.listdir(IMAGES_PATH))} - {filename}")
        end=time.time()
        print('All images loaded in: '+str(end-start)+'s')
