
from chess.pieces.base import Piece
from chess.move import Move


class Pawn(Piece):
    WHITE_PROMOTION_PIECES = ['Q', 'R', 'B', 'N']
    BLACK_PROMOTION_PIECES = ['q', 'r', 'b', 'n']

    def __init__(self, board, starting_location, white):
        symbol = 'P' if white else 'p'

        super().__init__(board, starting_location, white, symbol)

        self.promotion_pieces = self.WHITE_PROMOTION_PIECES if white else self.BLACK_PROMOTION_PIECES

    def pseudo_legal_moves(self):
        moves = []

        row, col = self.location

        direction = -1 if self.white else 1
        start_row = 6 if self.white else 1
        symbol = self.symbol
        promotion_rank = 0 if self.white else 7

        one_square_move = (row + direction, col)

        if self.board.in_bounds(one_square_move) and self.board.is_empty(one_square_move):
            if one_square_move[0] == promotion_rank:
                for promo in self.promotion_pieces:
                    moves.append(Move(self.location, one_square_move, piece=symbol, promotion=promo))
            else:
                moves.append(Move(self.location, one_square_move, piece=symbol))

            # 2 steps forward
            two_square_move = (row + 2 * direction, col)
            if row == start_row and self.board.in_bounds(two_square_move) and self.board.is_empty(two_square_move):
                moves.append(Move(self.location, two_square_move, symbol, pawn_moved_two_squares=True))

        # diagonal captures
        for diagonal_dir in (-1, 1):
            target_square = (row + direction, col + diagonal_dir)
            if not self.board.in_bounds(target_square):
                continue
            piece_on_tgt_sqr = self.board.get_piece(target_square)
            if piece_on_tgt_sqr and (piece_on_tgt_sqr.white != self.white):
                if target_square[0] == promotion_rank:
                    for promo in self.promotion_pieces:
                        moves.append(Move(self.location, target_square, symbol, capture=True,
                                          promotion=promo))
                else:
                    moves.append(Move(self.location, target_square, symbol, capture=True))
            else:
                # en passant
                if self.can_en_passant(target_square):
                    en_passant_square = self.can_en_passant(target_square)
                    moves.append(Move(self.location, target_square, symbol,
                                      capture=True,
                                      en_passant=True,
                                      captured_en_passant_square=en_passant_square))

        return moves

    def can_en_passant(self, target_square):
        if len(self.board.history) == 0:
            return None

        last_move = self.board.history[-1]
        if last_move.pawn_moved_two_squares:
            enemy_pawn_row, enemy_pawn_col = last_move.destination
            en_passant_row = enemy_pawn_row - 1 if self.white else enemy_pawn_row + 1
            en_passant_col = enemy_pawn_col

            if en_passant_row == target_square[0] and en_passant_col == target_square[1]:
                return last_move.destination

        return None
