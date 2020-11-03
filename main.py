import pygame, time
from memorykings.constants import WINDOW_WIDTH, WINDOW_HEIGHT, CORNER, CARD_SIZE
from memorykings.game import Game
from memorykings.board import Board, Card
from memorykings.player import Player
from memorykings.display import Display

import logging as log
log.basicConfig(level=log.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s")
#log.disable(log.CRITICAL)

GAME_WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Memory Kings')

def main():
    # GENERATING GAME
    run = True
    game = Game()
    game.setup_board(5,5)
    game.choose_colors()
    game.create_players(2)
    main_screen = Display()

    # GAME_LOOP
    while run:

        for event in pygame.event.get():
            if game.end_game_check():
                time.sleep(1)
                run = False

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game.all_pawns_set:
                game.place_pawns()

            if game.all_pawns_set:
                game.round(event)
                
            if game.end_turn == True:
                game.change_turn()
                            
            main_screen.print_grid(GAME_WINDOW, Card.deck, Player.array)
            main_screen.print_pawns(GAME_WINDOW, Player.array)
            main_screen.print_tokens(GAME_WINDOW, Player.array)
            pygame.display.update()

    pygame.quit()

main()
