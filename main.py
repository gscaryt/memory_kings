import pygame, time
from memorykings.constants import EXTRA_WIDTH, EXTRA_HEIGHT, CORNER, CARD_SIZE
from memorykings.game import Game
from memorykings.board import Board, Card
from memorykings.players import Player
from memorykings.display import Display

import logging as log
log.basicConfig(level=log.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s")
#log.disable(log.CRITICAL)

def main():
    # GENERATING GAME AND BOARD
    FPS = 60
    run = True
    clock = pygame.time.Clock()
    game = Game()
    main_screen = Display()
    game.setup_board(5)

    # SET THE BOARD SCREEN
    WINDOW_WIDTH, WINDOW_HEIGHT = EXTRA_WIDTH+game.board.cols*CARD_SIZE, EXTRA_HEIGHT+game.board.rows*CARD_SIZE
    GAME_WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Memory Kings')

    # GENERATE PLAYERS
    game.choose_colors()
    game.create_players(1) # Can change number from 1 (SOLO GAME) up to 4.

    # GAME_LOOP
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if game.end_game_check(Card.deck):
                time.sleep(1)
                run = False

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game.all_pawns_set:
                game.place_pawns()

            if game.all_pawns_set:
                game.round(GAME_WINDOW, main_screen)

            if game.end_turn == True:
                game.change_turn()
                            
            main_screen.print_all(GAME_WINDOW, game.board, Card.deck, Player.array)
    pygame.quit()

main()
