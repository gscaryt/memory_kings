import pygame
import logging as log
from .constants import CARD_SIZE, CORNER, PAWN_SIZE
from .player import Player
from .board import Board

log.basicConfig(level=log.DEBUG, format=" %(asctime)s -  %(levelname)s -  %(message)s")
#log.disable(log.CRITICAL)

class Game:
    def __init__(self):
        self.counter_turns = 0
        self.round_number = 0
        self.who_recruited = None
        self.player = []
        self.next_turn = 0
        self.pawn_selected = -1
        self.forward = True
        self.all_pawns_set = False


    def setup_board(self, cols, rows):
        self.board = Board(cols, rows)
        self.board.gen_grid()

    def choose_colors(self, color1='ORANGE', color2='PURPLE', color3='BLACK', color4='WHITE'):
        self.color_order = ('COUNTER', color1, color2, color3, color4)
        log.debug(f'choose_colors() - Chosen Colors: {self.color_order}')

    def create_players(self, num_of_players):
        for i in range(num_of_players+1):
            self.player.append(Player(i, self.color_order[i]))
            log.debug(f'create_players() - Player {self.player[i].order} - {self.player[i].color} created.')

    def place_pawns(self):
        if self.next_turn == 0 and len(self.player) != 2:
            self.next_turn += 1
        elif self.next_turn == 0 and len(self.player) == 2 and len(self.player[0].pawn) == 0:
            self.player[self.next_turn].place_pawn(self.board, 0, 0)
            self.change_turn()
        elif self.next_turn == 0 and len(self.player) == 2 and len(self.player[0].pawn) == 1:
            self.change_turn()
        else:
            click_pos = self.click_to_grid()
            self.player[self.next_turn].place_pawn(self.board, click_pos[0], click_pos[1])
            self.change_turn()
        self.all_pawns_set = bool(len(self.player[len(self.player)-1].pawn) == 2)
        if self.all_pawns_set:
            self.next_turn = 1

    def change_turn(self):
        if self.next_turn != len(self.player)-1:
            self.next_turn += 1
        else:
            self.next_turn = 0
        if self.next_turn == 0 and len(self.player) != 2:
            self.next_turn = 1
        self.forward = False
        log.debug(f'change_turn - Next Player: {self.next_turn}')

## SELECT

    def select_or_move(self):
        next_turn = self.next_turn
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if next_turn == 0:
            self.change_turn()
        elif next_turn == self.player[next_turn].order:
            if self.pawn_selected != -1:
                if not self.move():
                    log.debug(f'select_pawn() - Failed to move. Unselected.')
                    self.pawn_selected = -1
            else:
                for pawn_num in range(len(self.player[next_turn].pawn)):
                    coords = self.player[self.next_turn].get_pawn_screen_location(pawn_num)
                    log.debug(f'select_pawn() - Pawn {pawn_num}: {coords}')
                    log.debug(
                        f'select_pawn() - {click[0] == 1}'
                        f' {coords[0]-PAWN_SIZE < mouse[0] < coords[0]+PAWN_SIZE}'
                        f' and {coords[1]-PAWN_SIZE < mouse[1] < coords[1]+PAWN_SIZE}'
                        )
                    if (click[0] == 1 
                        and coords[0] < mouse[0] < coords[0]+PAWN_SIZE
                        and coords[1] < mouse[1] < coords[1]+PAWN_SIZE
                    ):
                        self.pawn_selected = pawn_num
                        log.debug(f'select_pawn() - Pawn Selected: {self.pawn_selected} is on the {self.board.card[self.player[next_turn].pawn[self.pawn_selected].position].rank} Card')
                        break
                    else:
                        self.pawn_selected = -1

## MOVEMENT

    def move(self):
        if self.pawn_selected != -1:
            click = pygame.mouse.get_pressed()
            if click[0] == 1:
                coordinates = self.click_to_grid()
                if coordinates != None:
                    if self.move_check(coordinates[0], coordinates[1]):
                        self.player[self.next_turn].pawn[self.pawn_selected].move_pawn(self.board, coordinates[0], coordinates[1])
                        self.pawn_selected = -1
                        self.forward = True
                        return True
                    else:
                        self.pawn_selected = -1
                        self.forward = False
                        return False
                else:
                    self.pawn_selected = -1
                    self.forward = False
                    return False

    def move_check(self, col, row):
        pawn = self.player[self.next_turn].pawn[self.pawn_selected]
        card = self.board.card[pawn.position]
        if (col, row) == (pawn.col, pawn.row):
            ## Move to Same Location Attempt
            log.debug("move_check() - Move to Same Location attempt. {card.rank}, {pawn.col}, {pawn.row} >> {col}, {row}")
            return False
        elif (
            ## Move as a Pawn (1 Orthogonal)
            (col, row) == (pawn.col+1, pawn.row) 
            or (col, row) == (pawn.col-1, pawn.row) 
            or (col, row) == (pawn.col, pawn.row+1) 
            or (col, row) == (pawn.col, pawn.row-1)
            ):
            log.debug(f"move_check() - Valid standard pawn move. {card.rank}, {pawn.col}, {pawn.row} >> {col}, {row}")
            return True
        else:
            ## Move from an Opponent's Card
            for i in range(len(self.player)):
                for j in range(len(self.player[i].token)):
                    token = self.player[i].token[j]
                    if ((token.col, token.row) == (pawn.col, pawn.row)
                        and not self.player[i].color == token.color):
                        log.debug(f"move_check() - Opponent token in place. Cannot escort. {card.rank}, {pawn.col}, {pawn.row} >> {col}, {row}")
                        return False
            ## Bishop Escort
            if ((card.rank == "Bishop") 
                and (abs(col - pawn.col) == abs(row - pawn.row))
                ):
                log.debug(f"move_check() - Valid Bishop Escort. {card.rank}, {pawn.col}, {pawn.row} >> {col}, {row}")
                return True
            ## Rook Escort
            elif ((card.rank == "Rook") 
                and ((col == pawn.col) or (row == pawn.row))
                ):
                log.debug(f"move_check() - Valid Rook Escort. {card.rank}, {pawn.col}, {pawn.row} >> {col}, {row}")
                return True
            ## Knight Escort
            elif ((card.rank == "Knight") 
                and ((abs(col-pawn.col) == 2 and abs(row-pawn.row) == 1) 
                or (abs(col-pawn.col) == 1 and abs(row-pawn.row) == 2))
                ):
                log.debug(f"move_check() - Valid Knight Escort. {card.rank}, {pawn.col}, {pawn.row} >> {col}, {row}")
                return True
            ## Queen Escort
            elif ((card.rank== "Queen") 
                and ((abs(col - pawn.col) == abs(row - pawn.row))
                or ((col == pawn.col) or (row == pawn.row)))
                ):
                log.debug(f"move_check() - Valid Queen Escort. {card.rank}, {pawn.col}, {pawn.row} >> {col}, {row}")
                return True
            ## Invalid Move
            else:
                log.debug(f"move_check() - Invalid Move. {card.rank}, {pawn.col}, {pawn.row} >> {col}, {row}")
                return False

    def counter_move(self):
        counter = self.player[0].pawn[0]
        if counter.row % 2 == 0 and not counter.col == self.board.cols-1:
            counter.move_pawn(self.board, counter.col+1, counter.row)
        elif counter.row % 2 != 0 and not counter.col == 0:
            counter.move_pawn(self.board, counter.col-1, counter.row)
        else:
            counter.move_pawn(self.board, counter.col, counter.row+1)
        self.forward = True

## RECRUIT

    def recruit_check(self):
        pawn = self.player[self.next_turn].pawn
        card = self.board.card
        if self.next_turn == 0:
            return
        if pawn[0].position != pawn[1].position:
            if (
                card[pawn[0].position].color == card[pawn[1].position].color
                and card[pawn[0].position].rank == card[pawn[1].position].rank
                ):
                if card[pawn[0].position].recruited != None:
                    log.debug(f"recruit_check() - These cards were already recruited by Player {card[pawn[0].position].recruited}")
                    return False
                else:
                    self.player[self.next_turn].place_tokens(self.board, pawn[0].col, pawn[0].row, pawn[1].col, pawn[1].row)
                    return True
            else:
                log.debug(f'recruit_check() - Cards are different.')
                return False
        else:
            log.debug(f'recruit_check() - Pawns are in the same card.')
            return False

    def counter_recruit(self):
        if len(self.player) == 2:
            counter = self.player[0].pawn[0]
            other_pawn = self.player[self.next_turn].pawn
            card = self.board.card[counter.position]
            for i in range(2):
                if (card.recruited == None 
                    and counter.position != other_pawn[i].position
                    and counter.color == other_pawn[i].color
                    and counter.rank == other_pawn[i].rank):
                    self.player[0].place_tokens(self.board, counter.col, counter.row, other_pawn[i].col, other_pawn[i].row)
                    log.debug('counter_recruit() - The counter recruited one pair.')
                    return True
                else:
                    return False

## END GAME

    def end_game_check(self):
        try:
            if self.player[0].pawn[0].position == 24:
                log.debug('The game is finished! Counter on the 25 card.')
                return True
            elif len(self.player) == 2:
                if self.player[0].score == 6:
                    log.debug('The game is finished! Counter recruited 6 pairs')
                    return True
                elif self.player[1].score == 6:
                    log.debug('The game is finished! You win with 6 pairs')
                    return True
            else:
                for i in range(len(self.player)-1):
                    if self.player[i].score == 12//(len(self.player)-1):
                        return True
            return False
        except: 
            pass

## INTERFACE

    def click_to_grid(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        click_pos = [0, 0]
        if click[0] == 1:
            if not (mouse[0] < CORNER[0] or mouse[1] < CORNER[1] 
                or mouse[0] > CORNER[0]+self.board.cols*CARD_SIZE
                or mouse[1] > CORNER[1]+self.board.rows*CARD_SIZE):
                for i in range(self.board.cols):
                    if i < (mouse[0]-150)/CARD_SIZE and (mouse[0]-150-CARD_SIZE)/CARD_SIZE < i:
                        click_pos[0] = i
                for j in range(self.board.rows):
                    if j < (mouse[1]-50)/CARD_SIZE and (mouse[1]-50-CARD_SIZE)/CARD_SIZE < j:
                        click_pos[1] = j
                log.debug(f'click_to_grid() - Mouse click on {mouse} represents the {click_pos} coordinates.')
                return click_pos
            else:
                log.debug(f'click_to_grid() - Mouse click outside the board.')
                return None



## TODO

    def queen_check(self):
        pass

    def get_game_state(self):
        pass

    def player_turn(self):
        pass

    def counter_turn(self):
        pass

    def round(self):
        pass
