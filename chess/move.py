
from dataclasses import dataclass

Square = tuple[int, int]  # (row, col)


@dataclass(frozen=True)
class Move:
    source: Square
    destination: Square
    piece: str  # white: 'P','R','N','B','Q','K', black: 'p','r','n','b','q','k'
    capture: bool = False
    pawn_moved_two_squares: bool = False
    promotion: str | None = None  # piece promoted to, if promotion
    en_passant: bool = False
    captured_en_passant_square: Square = None  # square of pawn captured in en passant
    castle_ks: bool = False
    castle_qs: bool = False
