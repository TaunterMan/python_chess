
class Piece:
    def __init__(self, board, starting_location, white, symbol):
        self.location = starting_location
        self.white = white
        self.board = board
        self.symbol = symbol
