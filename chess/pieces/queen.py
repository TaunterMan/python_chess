
from chess.pieces.sliding_pieces import SlidingPiece


class Queen(SlidingPiece):
    def __init__(self, board, starting_location, white):
        piece = 'Q' if white else 'q'
        move_directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        super().__init__(board, starting_location, white, piece, move_directions)
