import pygame

class Pawn:
    def __init__(self, board, color, col, row):
        self.color = color
        self.col = col
        self.row = row
        self.image = 'pawn_' + self.color + '.png'
        self.position = self.row*board.cols+self.col

    def move_pawn(self, board, col, row):
        self.record_position()
        self.col = col
        self.row = row
        self.position = row*board.cols+col
        print(f'The Pawn Moved: New Coordinates: {self.col, self.row}'
              f' New Position: {self.position}')

    def record_position(self):
        self.previous = self.position