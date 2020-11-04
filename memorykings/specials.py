import pygame, time
from .players import Player

class Power():
    def peek_card(self, window, display, board, card_array, player_array):
        print('Peek Card starts running.')
        display.print_all(window, board, card_array, player_array)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = board.click_to_grid()
                    if click_pos != None:
                        if not display.print_card(window, board, card_array, player_array, click_pos[0], click_pos[1]):
                            print('Failed to click a valid card.')
                            continue
                        else:
                            print('Print card.')
                            return True
        print('End of peek_card')

powers = Power()