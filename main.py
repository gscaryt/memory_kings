import pygame
import time
from memorykings.constants import EXTRA_WIDTH, EXTRA_HEIGHT, CORNER, CARD_SIZE, DARK_GREY, FPS
from memorykings.start_screen import start_menu
from memorykings.game import Game
from memorykings.board import Board, Card
from memorykings.players import Player
from memorykings.display import Display

import logging as log

FPS = 60

log.basicConfig(
    level=log.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s"
)
log.disable(log.CRITICAL)


def main():
    game = Game()
    start_menu(game)
    clock = pygame.time.Clock()
    run = True
    board = Board(game.grid_size[0], game.grid_size[1])
    board.gen_grid()

    display = Display()
    game.create_players()  # Can change number from 1 (SOLO GAME) up to 4


    WINDOW_WIDTH, WINDOW_HEIGHT = (
        EXTRA_WIDTH + board.cols * CARD_SIZE,
        EXTRA_HEIGHT + board.rows * CARD_SIZE,
    )
    GAME_WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Memory Kings")

    # GAME_LOOP
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            display.print_all(
                GAME_WINDOW, game, board, Card.deck, Player.array
            )
            if game.end_game_check():
                time.sleep(1)
                run = False
            if event.type == pygame.QUIT:
                run = False
            if game.all_pawns_set is not True:
                game.place_pawns(board, event)
            if game.all_pawns_set is True:
                game.round(GAME_WINDOW, board, display)
            if game.end_turn is True:
                game.change_turn()


    pygame.quit()


if __name__ == "__main__":
    main()
