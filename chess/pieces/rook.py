from chess.pieces.sliding_pieces import SlidingPiece


class Rook(SlidingPiece):
    def __init__(self, board, starting_location, white):
        symbol = 'R' if white else 'r'
        move_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        super().__init__(board, starting_location, white, symbol, move_directions)
        self.times_moved = 0  # needed for castling
