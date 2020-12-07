import pygame
from .constants import FONTS_PATH, BACKGROUND, WHITE
from .screens import blit_text, blit_image
from .assets import Asset

class Knmcd:
    def __init__(self):
        self.combo = 0
        self.active = False

    def code(self, display, event):
        if not self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.combo == 0:
                    self.combo += 1
                elif event.key == pygame.K_UP and self.combo == 1:
                    self.combo += 1
                elif event.key == pygame.K_DOWN and self.combo == 2:
                    self.combo += 1
                elif event.key == pygame.K_DOWN and self.combo == 3:
                    self.combo += 1
                elif event.key == pygame.K_LEFT and self.combo == 4:
                    self.combo += 1
                elif event.key == pygame.K_RIGHT and self.combo == 5:
                    self.combo += 1
                elif event.key == pygame.K_LEFT and self.combo == 6:
                    self.combo += 1
                elif event.key == pygame.K_RIGHT and self.combo == 7:
                    self.combo += 1
                elif event.key == pygame.K_b and self.combo == 8:
                    self.combo += 1
                elif event.key == pygame.K_a and self.combo == 9:
                    self.combo += 1
                else:
                    self.combo = 0
                
                if self.combo == 10:
                    self.active = True
                    self.message(display)

            elif (
                event.type == pygame.ACTIVEEVENT 
                or event.type == pygame.MOUSEMOTION 
                or event.type == pygame.VIDEORESIZE
            ):
                self.combo = 0

    def message(self, display):
        HINT = display.HINT
        DISP_W = display.DISP_W
        DISP_H = display.DISP_H
        border = pygame.rect.Rect(0,0,HINT*3.05, HINT*1.25)
        border.center = (DISP_W*0.5, DISP_H*0.5)
        pygame.draw.rect(display.WINDOW, (WHITE), border)
        rect = pygame.rect.Rect(0,0,HINT*3, HINT*1.2)
        rect.center = (DISP_W*0.5, DISP_H*0.5)
        pygame.draw.rect(display.WINDOW, (BACKGROUND), rect)
        DIMBO_L = pygame.font.Font(
            FONTS_PATH + "dimbo_regular.otf", int(HINT * 0.20)
        )
        blit_text(display.WINDOW, DIMBO_L, "Perfect Memory Activated!", DISP_W * 0.5, DISP_H * 0.5 - HINT*0.25)
        blit_image(display.WINDOW, Asset.image["queen_advice.png"], (DISP_W * 0.5, DISP_H * 0.5 + HINT*0.25), HINT * 0.50, HINT * 0.50)
        pygame.display.update()
        pygame.time.wait(2000)