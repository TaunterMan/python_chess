
from constants import WHITE_PIECES, BLACK_PIECES

from pieces.king import King
from pieces.queen import Queen
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.pawn import Pawn

from collections import Counter
from fen import fen_key


def alg_to_rc(alg: str) -> tuple[int, int]:
    file_ch, rank_ch = alg[0], alg[1]
    col = ord(file_ch) - ord('a')  # a to h -> 0..7
    row = 8 - int(rank_ch)  # 1 to 8 -> 7..0
    return row, col


def rc_to_alg(rc: tuple[int, int]) -> str:
    row, col = rc
    file_ch = chr(ord('a') + col)
    rank_ch = str(8 - row)
    return f"{file_ch}{rank_ch}"


class Board:
    def __init__(self):
        self.white_pieces = WHITE_PIECES
        self.black_pieces = BLACK_PIECES

        self.WIDTH = self.HEIGHT = 8

        self.white_king = King(self, alg_to_rc('e1'), True)
        self.white_queen = Queen(self, alg_to_rc('d1'), True)
        self.white_bishop1 = Bishop(self, alg_to_rc('c1'), True)
        self.white_bishop2 = Bishop(self, alg_to_rc('f1'), True)
        self.white_knight1 = Knight(self, alg_to_rc('b1'), True)
        self.white_knight2 = Knight(self, alg_to_rc('g1'), True)
        self.white_rook1 = Rook(self, alg_to_rc('a1'), True)
        self.white_rook2 = Rook(self, alg_to_rc('h1'), True)

        self.white_pawn1 = Pawn(self, alg_to_rc('a2'), True)
        self.white_pawn2 = Pawn(self, alg_to_rc('b2'), True)
        self.white_pawn3 = Pawn(self, alg_to_rc('c2'), True)
        self.white_pawn4 = Pawn(self, alg_to_rc('d2'), True)
        self.white_pawn5 = Pawn(self, alg_to_rc('e2'), True)
        self.white_pawn6 = Pawn(self, alg_to_rc('f2'), True)
        self.white_pawn7 = Pawn(self, alg_to_rc('g2'), True)
        self.white_pawn8 = Pawn(self, alg_to_rc('h2'), True)

        self.black_king = King(self, alg_to_rc('e8'), False)
        self.black_queen = Queen(self, alg_to_rc('d8'), False)
        self.black_bishop1 = Bishop(self, alg_to_rc('c8'), False)
        self.black_bishop2 = Bishop(self, alg_to_rc('f8'), False)
        self.black_knight1 = Knight(self, alg_to_rc('b8'), False)
        self.black_knight2 = Knight(self, alg_to_rc('g8'), False)
        self.black_rook1 = Rook(self, alg_to_rc('a8'), False)
        self.black_rook2 = Rook(self, alg_to_rc('h8'), False)

        self.black_pawn1 = Pawn(self, alg_to_rc('a7'), False)
        self.black_pawn2 = Pawn(self, alg_to_rc('b7'), False)
        self.black_pawn3 = Pawn(self, alg_to_rc('c7'), False)
        self.black_pawn4 = Pawn(self, alg_to_rc('d7'), False)
        self.black_pawn5 = Pawn(self, alg_to_rc('e7'), False)
        self.black_pawn6 = Pawn(self, alg_to_rc('f7'), False)
        self.black_pawn7 = Pawn(self, alg_to_rc('g7'), False)
        self.black_pawn8 = Pawn(self, alg_to_rc('h7'), False)

        self.white_objects = {self.white_king,
                              self.white_queen, self.white_bishop1, self.white_bishop2,
                              self.white_knight1, self.white_knight2, self.white_rook1, self.white_rook2,
                              self.white_pawn1, self.white_pawn2, self.white_pawn3, self.white_pawn4,
                              self.white_pawn5, self.white_pawn6, self.white_pawn7, self.white_pawn8}

        self.black_objects = {self.black_king,
                              self.black_queen, self.black_bishop1, self.black_bishop2,
                              self.black_knight1, self.black_knight2, self.black_rook1, self.black_rook2,
                              self.black_pawn1, self.black_pawn2, self.black_pawn3, self.black_pawn4,
                              self.black_pawn5, self.black_pawn6, self.black_pawn7, self.black_pawn8}

        self.pawns = [self.white_pawn1, self.white_pawn2, self.white_pawn3, self.white_pawn4,
                      self.white_pawn5, self.white_pawn6, self.white_pawn7, self.white_pawn8,
                      self.black_pawn1, self.black_pawn2, self.black_pawn3, self.black_pawn4,
                      self.black_pawn5, self.black_pawn6, self.black_pawn7, self.black_pawn8]

        self.board = [[None] * 8 for _ in range(8)]

        self.history = []  # list of Move objects
        self.positions = []  # list of FEN strings
        self.captured_pieces = []  # list of captured Piece objects
        self.promoted_pawns = []  # list of Pawn objects that have promoted

        self.half_move_clock = 0  # for fifty move rule and FEN
        self.full_move_number = 1  # for FEN
        self.ep_square = None  # square where en passant is possible, also for FEN

        self._pos_counts = Counter()  # position counts for threefold repetition
        self._pos_history = []  # history of position keys for unmaking moves

        # stacks for unmaking moves
        self._half_move_stack = []
        self._full_move_stack = []
        self._ep_stack = []

        self._record_position()

        self.checkmate = False
        self.stalemate = False

        self.white_to_move = True

        for piece in self.white_objects.union(self.black_objects):
            self.set_piece(piece.location, piece)

    def in_bounds(self, square: tuple[int, int]) -> bool:
        row, col = square
        return 0 <= row < self.HEIGHT and 0 <= col < self.WIDTH

    def get_piece(self, square) -> "Piece | None":
        row, col = square
        return self.board[row][col]

    def set_piece(self, square, piece):
        row, col = square
        self.board[row][col] = piece
        if piece:
            piece.location = square

    def is_empty(self, square: tuple[int, int]) -> bool:
        return self.get_piece(square) is None

    def make_move(self, move):
        # save state for unmaking move
        self._half_move_stack.append(self.half_move_clock)
        self._full_move_stack.append(self.full_move_number)
        self._ep_stack.append(self.ep_square)

        source = move.source
        destination = move.destination

        if not self.in_bounds(source) or not self.in_bounds(destination):
            raise ValueError(f"out of bounds: {source=} {destination=}")

        moving_piece = self.get_piece(source)
        if moving_piece is None:
            raise ValueError(f"No piece at {source}")

        target_piece = self.get_piece(destination)

        if move.en_passant:
            target_piece = self.get_piece(move.captured_en_passant_square)
            self.set_piece(move.captured_en_passant_square, None)

        if target_piece and target_piece.white == moving_piece.white:
            raise ValueError(f"Cannot move onto friendly piece at {destination}")

        if target_piece:
            (self.white_objects if target_piece.white else self.black_objects).discard(target_piece)
            target_piece.location = None

        self.set_piece(source, None)
        self.set_piece(destination, moving_piece)

        if move.promotion:
            promoted_pawn = moving_piece
            if move.promotion == 'Q':
                promoted_piece = Queen(self, destination, moving_piece.white)
            elif move.promotion == 'R':
                promoted_piece = Rook(self, destination, moving_piece.white)
            elif move.promotion == 'B':
                promoted_piece = Bishop(self, destination, moving_piece.white)
            elif move.promotion == 'N':
                promoted_piece = Knight(self, destination, moving_piece.white)

            (self.white_objects if moving_piece.white else self.black_objects).discard(moving_piece)
            (self.white_objects if moving_piece.white else self.black_objects).add(promoted_piece)

            self.set_piece(destination, promoted_piece)

            moving_piece.location = None
            self.promoted_pawns.append(promoted_pawn)

        if move.castle_ks:
            if moving_piece.white:
                rook_source = alg_to_rc('h1')
                rook_destination = alg_to_rc('f1')
            else:
                rook_source = alg_to_rc('h8')
                rook_destination = alg_to_rc('f8')
            rook = self.get_piece(rook_source)
            self.set_piece(rook_source, None)
            self.set_piece(rook_destination, rook)
            if hasattr(rook, "times_moved"):
                rook.times_moved += 1

        if move.castle_qs:
            if moving_piece.white:
                rook_source = alg_to_rc('a1')
                rook_destination = alg_to_rc('d1')
            else:
                rook_source = alg_to_rc('a8')
                rook_destination = alg_to_rc('d8')
            rook = self.get_piece(rook_source)
            self.set_piece(rook_source, None)
            self.set_piece(rook_destination, rook)
            if hasattr(rook, "times_moved"):
                rook.times_moved += 1

        if hasattr(moving_piece, "times_moved"):
            moving_piece.times_moved += 1

        self.history.append(move)
        self.captured_pieces.append(target_piece)

        self.white_to_move = not self.white_to_move

        # en passant target for next move
        self.ep_square = None
        if getattr(move, "pawn_moved_two_squares", False):
            sr, sc = source
            dr, dc = destination
            self.ep_square = ((sr + dr) // 2, sc)

        # Half move clock (resets on pawn move or capture)
        moved_is_pawn = moving_piece.symbol.lower() == 'p'
        did_capture = (target_piece is not None) or move.en_passant
        if moved_is_pawn or did_capture:
            self.half_move_clock = 0
        else:
            self.half_move_clock += 1

        # Full move number increments after Black's move
        if self.white_to_move:
            self.full_move_number += 1

        # Record position for threefold
        self._record_position()

        return target_piece

    def unmake_move(self):
        if len(self.history) == 0:
            return

        if self._pos_history:
            last = self._pos_history.pop()
            self._pos_counts[last] -= 1
            if self._pos_counts[last] <= 0:
                del self._pos_counts[last]

        move_to_undo = self.history[-1]
        captured_piece = self.captured_pieces[-1]
        source = move_to_undo.source
        destination = move_to_undo.destination

        if move_to_undo.promotion:
            original_pawn = self.promoted_pawns.pop()
            promoted_piece = self.get_piece(destination)

            (self.white_objects if promoted_piece.white else self.black_objects).discard(promoted_piece)
            self.set_piece(destination, None)
            promoted_piece.location = None

            (self.white_objects if promoted_piece.white else self.black_objects).add(original_pawn)
            self.set_piece(source, original_pawn)
            piece = original_pawn

            if move_to_undo.capture and captured_piece is not None:
                (self.white_objects if captured_piece.white else self.black_objects).add(captured_piece)
                self.set_piece(destination, captured_piece)
        else:
            piece = self.get_piece(destination)
            self.set_piece(source, piece)

            if move_to_undo.en_passant:
                if captured_piece is not None:
                    (self.white_objects if captured_piece.white else self.black_objects).add(captured_piece)
                self.set_piece(move_to_undo.captured_en_passant_square, captured_piece)
                self.set_piece(destination, None)
            elif move_to_undo.capture:
                if captured_piece is not None:
                    (self.white_objects if captured_piece.white else self.black_objects).add(captured_piece)
                self.set_piece(destination, captured_piece)
            else:
                self.set_piece(destination, None)

        if move_to_undo.castle_ks:
            if piece.white:
                rook_source = alg_to_rc('h1')
                rook_destination = alg_to_rc('f1')
            else:
                rook_source = alg_to_rc('h8')
                rook_destination = alg_to_rc('f8')
            rook = self.get_piece(rook_destination)
            self.set_piece(rook_destination, None)
            self.set_piece(rook_source, rook)
            if hasattr(rook, "times_moved"):
                rook.times_moved -= 1
        if move_to_undo.castle_qs:
            if piece.white:
                rook_source = alg_to_rc('a1')
                rook_destination = alg_to_rc('d1')
            else:
                rook_source = alg_to_rc('a8')
                rook_destination = alg_to_rc('d8')
            rook = self.get_piece(rook_destination)
            self.set_piece(rook_destination, None)
            self.set_piece(rook_source, rook)
            if hasattr(rook, "times_moved"):
                rook.times_moved -= 1

        if hasattr(piece, "times_moved"):
            piece.times_moved -= 1

        self.history.pop()
        self.captured_pieces.pop()

        self.white_to_move = not self.white_to_move
        self.half_move_clock = self._half_move_stack.pop()
        self.full_move_number = self._full_move_stack.pop()
        self.ep_square = self._ep_stack.pop()

    def legal_moves(self):
        check_white_king = self.white_to_move  # on white's turn, we need to check if the white king is in check
        in_check_before_moving = self.check(check_white_king)

        legal_moves = []
        pieces = self.white_objects if check_white_king else self.black_objects
        for piece in pieces:
            moves = piece.pseudo_legal_moves()
            if moves:
                for move in moves:
                    self.make_move(move)
                    if not self.check(check_white_king):
                        if not (in_check_before_moving and (move.castle_ks or move.castle_qs)):
                            legal_moves.append(move)
                    self.unmake_move()

        if len(legal_moves) == 0:
            if in_check_before_moving:
                self.checkmate = True
            else:
                self.stalemate = True

        return legal_moves

    def get_enemy_pieces(self, white):
        if white:
            return self.black_objects
        else:
            return self.white_objects

    def get_king(self, white):
        if white:
            return self.white_king.location
        else:
            return self.black_king.location

    def check(self, check_white_king):
        enemy_pieces = self.get_enemy_pieces(check_white_king)
        check = False

        for piece in enemy_pieces:
            moves = piece.pseudo_legal_moves()
            if moves:
                for move in moves:
                    if move.destination == self.get_king(check_white_king):
                        check = True

        return check

    def check_insufficient_material(self):
        # Count remaining pieces
        white_pieces = [piece.symbol for piece in self.white_objects]
        black_pieces = [piece.symbol for piece in self.black_objects]

        # Only kings
        if len(white_pieces) == 1 and len(black_pieces) == 1:
            return True

        # King and one minor piece vs. king
        minor_pieces = {'B', 'N'}
        if (len(white_pieces) == 2 and white_pieces[1] in minor_pieces and len(black_pieces) == 1) or \
                (len(black_pieces) == 2 and black_pieces[1] in minor_pieces and len(white_pieces) == 1):
            return True

        # King and two knights vs. king (for both sides)
        if (len(white_pieces) == 3 and sorted(white_pieces[1:]) == ['N', 'N'] and len(black_pieces) == 1) or \
                (len(black_pieces) == 3 and sorted(black_pieces[1:]) == ['n', 'n'] and len(white_pieces) == 1):
            return True

        return False

    def check_fifty_move_rule(self):
        return self.half_move_clock >= 100

    def _record_position(self):
        key = fen_key(self)
        self._pos_history.append(key)
        self._pos_counts[key] += 1

    def check_threefold_repetition(self) -> bool:
        return self._pos_counts.get(fen_key(self), 0) >= 3
