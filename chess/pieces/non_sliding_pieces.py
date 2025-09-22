
from chess.pieces.base import Piece
from chess.move import Move


class NonSlidingPiece(Piece):
    def __init__(self, board, starting_location, white, symbol, move_directions):
        self.move_directions = move_directions
        super().__init__(board, starting_location, white, symbol)

    def candidate_moves(self):
        row, col = self.location
        candidate_moves = []

        for move_direction in self.move_directions:
            candidate_moves.append((row + move_direction[0], col + move_direction[1]))

        return candidate_moves

    def pseudo_legal_moves(self):
        candidate_moves = self.candidate_moves()
        moves = []
        for square in candidate_moves:
            if self.board.in_bounds(square):
                if self.board.is_empty(square):
                    moves.append(Move(self.location, square, self.symbol))
                else:
                    if self.board.get_piece(square) in self.board.get_enemy_pieces(self.white):
                        moves.append(Move(self.location, square, self.symbol, capture=True))

        return moves
