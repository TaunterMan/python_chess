
from chess.pieces.non_sliding_pieces import NonSlidingPiece
from chess.move import Move


class King(NonSlidingPiece):
    def __init__(self, board, starting_location, white):
        symbol = 'K' if white else 'k'

        self.times_moved = 0

        move_directions = [(-1, -1), (-1, 0), (-1, 1),
                           (0, -1), (0, 1),
                           (1, -1), (1, 0), (1, 1)]

        super().__init__(board, starting_location, white, symbol, move_directions)

    def pseudo_legal_moves(self):
        moves = super().pseudo_legal_moves()
        if self.can_castle_kingside():
            moves.append(Move(self.location, (self.location[0], self.location[1] + 2), self.symbol,
                              castle_ks=True))
        if self.can_castle_queenside():
            moves.append(Move(self.location, (self.location[0], self.location[1] - 2), self.symbol,
                              castle_qs=True))
        return moves

    def can_castle_kingside(self):
        if self.times_moved > 0:
            return False

        row = 7 if self.white else 0

        corner_piece = self.board.get_piece((row, 7))

        if corner_piece is None or corner_piece.symbol not in ('R', 'r'):
            return False

        rook = corner_piece

        if self.location == (row, 4):  # Check if king is in starting position
            # Makes sure rook hasn't moved, spaces between are empty, and no squares are under attack
            if (rook.times_moved == 0 and self.board.is_empty((row, 5))
                    and self.board.is_empty((row, 6))):
                return True
            else:
                return False

    def can_castle_queenside(self):
        if self.times_moved > 0:
            return False

        rank = 7 if self.white else 0

        corner_piece = self.board.get_piece((rank, 0))

        if corner_piece is None or corner_piece.symbol not in ('R', 'r'):
            return False

        rook = corner_piece

        if self.white:
            if self.location == (rank, 4):  # Check if king is in starting position
                # Makes sure rook hasn't moved, spaces between are empty, and no squares are under attack
                if (rook.times_moved == 0 and self.board.is_empty((rank, 3))
                        and self.board.is_empty((rank, 2)) and self.board.is_empty((rank, 1))):
                    return True
                else:
                    return False
