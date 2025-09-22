
from chess.pieces.non_sliding_pieces import NonSlidingPiece


class Knight(NonSlidingPiece):
    def __init__(self, board, starting_location, white):
        symbol = 'N' if white else 'n'

        move_directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        super().__init__(board, starting_location, white, symbol, move_directions)
