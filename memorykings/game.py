import pygame, time
from .constants import CARD_SIZE, PAWN_SIZE, CORNER, GRID
from .player import Player, CounterKing
from .board import Board, Card

import logging as log
log.basicConfig(level=log.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s")
log.disable(log.CRITICAL)

class Game:
    def setup_board(self, cols, rows):
        self.board = Board(cols, rows)
        self.board.gen_grid()

    def choose_colors(self, color1='PURPLE', color2='BLACK', color3='WHITE', color4='ORANGE'):
        self.color_order = ('COUNTER', color1, color2, color3, color4)
        log.debug(f'choose_colors() - Chosen Colors: {self.color_order}')

    def create_players(self, num_of_players):
        '''Start by creating a CounterKing in the 0th Player.array position\n
        then create the other players.'''
        counter = CounterKing(0, "COUNTER")
        log.debug(f'create_players() - Player {counter.order} - {counter.color} created.')
        log.debug(f'{Player.array}')

        for i in range(1, num_of_players+1):
            player = Player(i, self.color_order[i])
            log.debug(f'create_players() - Player {player.order} - {player.color} created.')
        self.num_of_players = len(Player.array)
        log.debug(f'{Player.array}')

        self.current_turn = 0
        self.current_player = Player.array[self.current_turn]
        self.counter = Player.array[0]
        self.all_pawns_set = False
        self.end_turn = False

    def place_pawns(self):
            if not self.all_pawns_set:
                if self.num_of_players == 2 and self.current_turn == 0:
                    '''If this is a Solo game, and the CounterKing has no pawns, place the Counter pawn'''
                    if len(self.current_player.pawn) == 0:
                        self.current_player.place_pawn()
                        self.change_turn()
                    else:
                        self.change_turn()
                else:
                    '''If this is a Multiplayer game (num_of_players >2), skip the turn 0\n
                    and place a Player's Pawn until all pawns of all players were placed.'''
                    if self.num_of_players > 2 and self.current_turn == 0:
                        self.current_turn += 1
                        self.current_player = Player.array[self.current_turn]
                    else:
                        click_pos = self.board.click_to_grid()
                        self.current_player.place_pawn(self.board, click_pos[0], click_pos[1])
                        self.change_turn()
                
                '''self.all_pawns_set returns True if the last player has placed all their 2 pawns'''
                last_player = Player.array[self.num_of_players-1]
                self.all_pawns_set = bool(len(last_player.pawn) == 2)
                if self.all_pawns_set:
                    self.current_turn = 1
                    self.pawn_selected = False
                    log.debug(f'place_pawns() - All pawns set: {self.all_pawns_set}')
            else:
                return

## SELECT/MOVE

    def select(self, event):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.pawn_selected:
                click_pos = self.board.click_to_grid()
                if not self.pawn_selected.move(self.board, Card.deck, click_pos[0], click_pos[1]):
                    log.debug(f'select() - Failed to move. Unselected.')
                    self.pawn_selected = False
                else:
                    log.debug(f'select() - Successful move. Unselected and end_turn (unless recruited).')
                    self.pawn_selected = False
                    self.end_turn = True

            else:
                self.current_player = Player.array[self.current_turn]
                log.debug(f'select() - Current Turn: {self.current_turn}')
                for pawn_num, pawn in enumerate(self.current_player.pawn):
                    coords = pawn.get_screen_location(pawn_num, self.current_turn)
                    log.debug(f'select() - Pawn {pawn_num}: {coords}')
                    log.debug(
                        f'select() -'
                        f' {coords[0]-PAWN_SIZE < mouse[0] < coords[0]+PAWN_SIZE}'
                        f' and {coords[1]-PAWN_SIZE < mouse[1] < coords[1]+PAWN_SIZE}'
                        f' {mouse}')
                    if (click[0] == 1 
                        and coords[0] < mouse[0] < coords[0]+PAWN_SIZE
                        and coords[1] < mouse[1] < coords[1]+PAWN_SIZE
                    ):
                        self.pawn_selected = self.current_player.pawn[pawn_num]
                        self.end_turn = False
                        log.debug(f'select() - Pawn Selected: {self.pawn_selected} is on the {Card.deck[self.pawn_selected.position]} Card')
                        break
                    else:
                        self.pawn_selected = False
                        self.end_turn = False

## GAME FLOW

    def change_turn(self):
        '''Increases the current turn up to the last player\n
        and then back to 0.'''
        if self.current_turn < self.num_of_players-1:
            self.current_turn += 1
        else:
            self.current_turn = 0

        if self.current_turn == 0 and self.num_of_players > 2:
            '''If multiplayer, skip the CounterKing turn (0)'''
            self.current_turn = 1
        
        self.current_player = Player.array[self.current_turn]
        self.end_turn = False
        log.debug(f'change_turn - Next Player: {self.current_player.color}')

    def round(self, event):
        if self.num_of_players == 2 and Player.recruited == 0:
            time.sleep(0.05)
            self.counter.pawn[0].move(self.board)
            self.recruit_check()
        if self.num_of_players == 2 and self.current_turn == 0:
            time.sleep(0.05)
            self.counter.pawn[0].move(self.board)
            self.end_turn = True
            self.recruit_check()
        else:
            self.select(event)
            Player.recruited = None
            self.recruit_check()

## CHECKS

    def recruit_check(self):
        if self.num_of_players == 2:
            self.counter.recruit(self.board, Card.deck)
        if Player.recruited == None:
            self.current_player.recruit(self.board, Card.deck)
        if Player.recruited != None:
            self.current_turn = Player.recruited
            self.current_player = Player.array[self.current_turn]
            self.end_turn = False

    def end_game_check(self):
        try:
            if Player.array[0].pawn[0].position == 24:
                log.debug('end_game_check() - The game is finished! Counter on the 25 card.')
                return True
            elif self.num_of_players == 2:
                if Player.array[0].score == 6:
                    log.debug('end_game_check() - The game is finished! Counter recruited 6 pairs')
                    return True
                elif Player.array[1].score == 6:
                    log.debug('end_game_check() - The game is finished! You won with 6 pairs')
                    return True
            else:
                for player in Player.array:
                    if player.score == 12//(self.num_of_players-1):
                        log.debug('end_game_check() - The game is finished! You won!')
                        return True
            return False
        except: 
            pass

## TODO

    def queen_check(self):
        pass