import pygame

class Pawn:
    def __init__(self, board, color, col, row):
        self.color = color
        self.col = col
        self.row = row
        self.image = 'pawn_' + self.color + '.png'
        self.position = self.row*board.cols+self.col

    def move(self, board, col, row):
        self.record_position()
        self.col = col
        self.row = row
        self.position = row*board.cols+col
        print(f'The Pawn Moved: New Coordinates: {self.col, self.row}'
              f' New Position: {self.position}')

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