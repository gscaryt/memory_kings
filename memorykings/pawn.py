import pygame

class Pawn:
    def __init__(self, color, col, row, board_cols):
        self.color = color
        self.col = col
        self.row = row
        self.image = 'pawn_' + color + '.png'
        self.position = self.row*board_cols+self.col

    def move(self, col, row):
        self.record_position()
        self.col = col
        self.row = row

    def record_position(self):
        self.previous = self.position



"""    def select(self, col, row, player):
        if self.selected:
            result = self.move(col, row)
            if not result:
                self.selected = None
                self.select(col, row, player)

            return True
        return False"""