from chess.pieces.base import Piece
from chess.move import Move


class SlidingPiece(Piece):
    def __init__(self, board, starting_location, white, symbol, move_directions):
        self.move_directions = move_directions
        super().__init__(board, starting_location, white, symbol)

    def pseudo_legal_moves(self):
        r0, c0 = self.location
        moves = []

        for dr, dc in self.move_directions:
            r, c = r0 + dr, c0 + dc
            while self.board.in_bounds((r, c)):
                piece_on_square = self.board.get_piece((r, c))
                if piece_on_square is None:
                    moves.append(Move(self.location, (r, c), self.symbol))
                else:
                    if piece_on_square.white != self.white:
                        moves.append(Move(self.location, (r, c), self.symbol, capture=True))
                    break

                r += dr
                c += dc

        return moves
