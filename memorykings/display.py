import pygame
import logging as log
from .constants import CARD_SIZE, IMAGES_PATH, CORNER, DARK_GREY, PAWN_SIZE, TOKEN_SIZE
from .card import Card
from .player import Player

import logging as log
log.basicConfig(level=log.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s")
#log.disable(log.CRITICAL)

class Display:
    def __init__(self):
        pass
    
    def get_image(self, image, width, height):
        return pygame.transform.scale(pygame.image.load(IMAGES_PATH + image), (width, height))
    
    def print_grid(self, window, board, player_array):
        card_array = board.card
        window.fill(DARK_GREY)
        for card_position in range(len(card_array)):
            card = card_array[card_position]
            col, row = card.col, card.row
            coords_on_screen = CORNER[0]+CARD_SIZE*col, CORNER[1]+CARD_SIZE*row
            is_open = False
            for i in range(len(player_array)):
                player = player_array[i]
                for j in range(len(player.pawn)):
                    for k in range(len(player.token)):
                        if player.token[k].position == card_position:
                            card_image = self.get_image(card.image, CARD_SIZE, CARD_SIZE)
                            window.blit(card_image, coords_on_screen)
                            is_open = True
                    if player.pawn[j].position == card_position:
                        card_image = self.get_image(card.image, CARD_SIZE, CARD_SIZE)
                        window.blit(card_image, coords_on_screen)
                        is_open = True
            if not is_open:
                if card.back == 'White':
                    white_back = self.get_image('white_back.png', CARD_SIZE, CARD_SIZE)
                    window.blit(white_back, coords_on_screen)
                elif card.back == 'Black':
                    black_back = self.get_image('black_back.png', CARD_SIZE, CARD_SIZE)
                    window.blit(black_back, coords_on_screen)

    def print_pawns(self, window, player_array):
        for i in range(len(player_array)):
            for j in range(len(player_array[i].pawn)):
                pawn = player_array[i].pawn[j]
                coords_on_screen = player_array[i].get_pawn_screen_location(j)
                pawn_image = self.get_image(pawn.image, PAWN_SIZE, PAWN_SIZE)
                window.blit(pawn_image, coords_on_screen)

    def print_tokens(self, window, player_array):
        for i in range(len(player_array)):
            for j in range(len(player_array[i].token)):
                token = player_array[i].token[j]
                coords_on_screen = (
                    (CORNER[0]+CARD_SIZE*(1+token.col))-(TOKEN_SIZE)-5,
                    (CORNER[1]+CARD_SIZE*(token.row))+(TOKEN_SIZE)-15
                    )
                token_image = self.get_image(token.image, TOKEN_SIZE, TOKEN_SIZE)
                window.blit(token_image, coords_on_screen)