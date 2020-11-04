import pygame, time
from .constants import CARD_SIZE, IMAGES_PATH, CORNER, DARK_GREY, PAWN_SIZE, TOKEN_SIZE

import logging as log
log.basicConfig(level=log.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s")
log.disable(log.CRITICAL)

class Display:
    def get_image(self, image, width, height):
        return pygame.transform.scale(pygame.image.load(IMAGES_PATH + image), (width, height))
    
    def print_grid(self, window, board, card_array, player_array):
        window.fill(DARK_GREY)
        for i in range(board.cols*board.rows):
            card = card_array[i]
            coords_on_screen = CORNER[0]+CARD_SIZE*card.col, CORNER[1]+CARD_SIZE*card.row
            is_open = False
            for player in player_array:
                for pawn in player.pawn:
                    for token in player.token:
                        if token.position == card.position:
                            card_image = self.get_image(card.image, CARD_SIZE, CARD_SIZE)
                            window.blit(card_image, coords_on_screen)
                            is_open = True
                    if pawn.position == card.position:
                        card_image = self.get_image(card.image, CARD_SIZE, CARD_SIZE)
                        window.blit(card_image, coords_on_screen)
                        is_open = True
            if not is_open:
                if card.back == 'WHITE':
                    white_back = self.get_image('white_back.png', CARD_SIZE, CARD_SIZE)
                    window.blit(white_back, coords_on_screen)
                elif card.back == 'BLACK':
                    black_back = self.get_image('black_back.png', CARD_SIZE, CARD_SIZE)
                    window.blit(black_back, coords_on_screen)

    def print_pawns(self, window, player_array):
        for player_num, player in enumerate(player_array):
            for pawn_num, pawn in enumerate(player.pawn):
                coords_on_screen = pawn.get_screen_location(pawn_num, player_num)
                pawn_image = self.get_image(player.pawn[pawn_num].image, PAWN_SIZE, PAWN_SIZE)
                window.blit(pawn_image, coords_on_screen)

    def print_tokens(self, window, player_array):
        for player in player_array:
            for token in player.token:
                coords_on_screen = (
                    (CORNER[0]+CARD_SIZE*(1+token.col))-(TOKEN_SIZE)-5,
                    (CORNER[1]+CARD_SIZE*(token.row))+(TOKEN_SIZE)-15
                    )
                token_image = self.get_image(token.image, TOKEN_SIZE, TOKEN_SIZE)
                window.blit(token_image, coords_on_screen)

    def print_all(self, window, board, card_array, player_array):
        self.print_grid(window, board, card_array, player_array)
        self.print_pawns(window, player_array)
        self.print_tokens(window, player_array)
        pygame.display.update()
    
    def print_card(self, window, board, card_array, player_array, col, row):
        card = board.grid[row][col]
        coords_on_screen = CORNER[0]+CARD_SIZE*col, CORNER[1]+CARD_SIZE*row
        is_open = False
        for player in player_array:
            for pawn in player.pawn:
                for token in player.token:
                    if token.position == card.position:
                        is_open = True
                        return False
                if pawn.position == card.position:
                    is_open = True
                    return False
        if not is_open:
            card_image = self.get_image(card.image, CARD_SIZE, CARD_SIZE)
            window.blit(card_image, coords_on_screen)
            pygame.display.update()
            time.sleep(1.5)
            return True

