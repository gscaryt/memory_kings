import pygame, time
from .players import Player

import logging as log
log.basicConfig(level=log.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s")
#log.disable(log.CRITICAL)

class Power():
    def peek_card(self, window, display, game, board, card_array, player_array):
        log.debug('Peek Card starts running.')
        display.print_all(window, game, board, card_array, player_array)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = board.click_to_grid()
                    if click_pos != None:
                        if not display.print_card(window, board, card_array, player_array, click_pos[0], click_pos[1]):
                            log.debug('Failed to click a valid card.')
                            continue
                        else:
                            print('Print card.')
                            return True
        log.debug('End of peek_card')

powers = Power()