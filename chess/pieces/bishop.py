
from chess.pieces.sliding_pieces import SlidingPiece


class Bishop(SlidingPiece):
    def __init__(self, board, starting_location, white):
        piece = 'B' if white else 'b'
        move_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        super().__init__(board, starting_location, white, piece, move_directions)
