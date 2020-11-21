import pygame
import os
import time
from .constants import IMAGES_PATH, FONTS_PATH, SOUNDS_PATH


class Asset:
    image = {}
    sound = {}
    _mute_sounds = False

    def __init__(self, display):
        start = time.time()
        pygame.font.init()
        pygame.mixer.init()
        DIMBO_L = pygame.font.Font(FONTS_PATH + "dimbo_regular.ttf", int(15))
        if len(Asset.image) == len(os.listdir(IMAGES_PATH)):
            print("Reseting the game. Images are already loaded.")
            text = DIMBO_L.render(
                "All Images ready. Move your mouse to continue.", True, (255, 255, 255)
            )
            display.WINDOW.fill((0, 0, 0))
            display.WINDOW.blit(text, (20, 20))
            pygame.display.update()
        else:
            for i, filename in enumerate(os.listdir(IMAGES_PATH)):
                if filename.endswith(".png"):
                    Asset.image[filename] = pygame.image.load(
                        IMAGES_PATH + filename
                    ).convert_alpha()
                    print(
                        f"Loading Images: {i+1}/{len(os.listdir(IMAGES_PATH))} - {filename}"
                    )
                    display.WINDOW.fill((0, 0, 0))
                    text = DIMBO_L.render(
                        f"Loading Images: {i+1}/{len(os.listdir(IMAGES_PATH))}",
                        True,
                        (255, 255, 255),
                    )
                    display.WINDOW.blit(text, (20, 20))
                    pygame.display.update()
            for i, filename in enumerate(os.listdir(SOUNDS_PATH)):
                if filename.endswith(".wav"):
                    Asset.sound[filename] = pygame.mixer.Sound(SOUNDS_PATH + filename)
                    print(
                        f"Loading Sounds: {i+1}/{len(os.listdir(SOUNDS_PATH))} - {filename}"
                    )
                    display.WINDOW.fill((0, 0, 0))
                    text = DIMBO_L.render(
                        f"Loading Sounds: {i+1}/{len(os.listdir(SOUNDS_PATH))}",
                        True,
                        (255, 255, 255),
                    )
                    display.WINDOW.blit(text, (20, 20))
                    pygame.display.update()
            end = time.time()
            print(f"All assets loaded in: {str(end-start)}s")
            display.WINDOW.fill((0, 0, 0))
            text = DIMBO_L.render(
                f"All {len(os.listdir(IMAGES_PATH)) + len(os.listdir(SOUNDS_PATH))} Assets ready.",
                True,
                (255, 255, 255),
            )
            display.WINDOW.blit(text, (20, 20))
            pygame.display.update()

def sound(filename):
    if Asset._mute_sounds == False:
        Asset.sound[filename].set_volume(0.3)
        Asset.sound[filename].play()