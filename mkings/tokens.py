class Token:
    def __init__(self, color, col, row):
        self.color = color
        self.col = col
        self.row = row
        self.image = "token_" + color + ".png"

    @property
    def position(self):
        return (self.col, self.row)