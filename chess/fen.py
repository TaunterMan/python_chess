from __future__ import annotations
from typing import Callable, Optional, Any

Square = tuple[int, int]
FILES = "abcdefgh"


def rc_to_alg(rc: Square) -> str:
    r, c = rc
    return f"{FILES[c]}{8 - r}"


def alg_to_rc(alg: str) -> Square:
    f, r = alg[0], alg[1]
    return 8 - int(r), FILES.index(f)


def _ep_target_if_capturable(board) -> Optional[Square]:
    # Return the en-passant target square ONLY if side-to-move can actually capture en passant now.
    ep = getattr(board, "ep_square", None)
    if ep is None:
        return None

    r, c = ep
    if board.white_to_move:
        src_row = r + 1
        want = 'P'
    else:
        src_row = r - 1
        want = 'p'

    for dc in (-1, 1):
        sq = (src_row, c + dc)
        if 0 <= sq[0] < 8 and 0 <= sq[1] < 8:
            p = board.get_piece(sq)
            if p and p.symbol == want:
                return ep
    return None


def _castling_rights_string(board) -> str:
    # Derive 'KQkq' (castling legality) from kings/rooks on start squares and their times_moved flags
    rights: list[str] = []

    wk = getattr(board, "white_king", None)
    bk = getattr(board, "black_king", None)

    # White side
    if wk and getattr(wk, "times_moved", 1) == 0 and board.get_piece((7, 4)) is wk:
        rh1 = board.get_piece((7, 7))
        ra1 = board.get_piece((7, 0))
        if rh1 and rh1.white and getattr(rh1, "times_moved", 1) == 0:
            rights.append('K')
        if ra1 and ra1.white and getattr(ra1, "times_moved", 1) == 0:
            rights.append('Q')

    # Black side
    if bk and getattr(bk, "times_moved", 1) == 0 and board.get_piece((0, 4)) is bk:
        rh8 = board.get_piece((0, 7))
        ra8 = board.get_piece((0, 0))
        if rh8 and (not rh8.white) and getattr(rh8, "times_moved", 1) == 0:
            rights.append('k')
        if ra8 and (not ra8.white) and getattr(ra8, "times_moved", 1) == 0:
            rights.append('q')

    return "".join(rights) if rights else "-"


def to_fen(board, *, normalize_ep: bool = False) -> str:
    """Return a full FEN. If normalize_ep=True, EP is '-' unless an EP capture is currently legal."""
    # piece placement (ranks 8→1 are rows 0→7)
    ranks: list[str] = []
    for r in range(8):
        empties = 0
        out: list[str] = []
        for c in range(8):
            p = board.get_piece((r, c))
            if p is None:
                empties += 1
            else:
                if empties:
                    out.append(str(empties))
                    empties = 0
                out.append(p.symbol)
        if empties:
            out.append(str(empties))
        ranks.append("".join(out))
    placement = "/".join(ranks)

    # active color
    active = "w" if getattr(board, "white_to_move", True) else "b"

    # castling rights
    castling = _castling_rights_string(board)

    # en passant target square
    if normalize_ep:
        ep_sq = _ep_target_if_capturable(board)
    else:
        ep_sq = getattr(board, "ep_square", None)
    ep = rc_to_alg(ep_sq) if ep_sq is not None else "-"

    # 5/6) Clocks
    half = str(getattr(board, "half_move_clock", 0))
    full = str(getattr(board, "full_move_number", 1))

    return f"{placement} {active} {castling} {ep} {half} {full}"


def from_fen(
        board,
        fen: str,
        piece_factory: Callable[[Any, str, Square], object] | None = None,
) -> None:
    # load a FEN position *into the given board*, replacing its current state.
    # `piece_factory(board, symbol, square)` must return a Piece object for FEN symbol at `square`.
    fields = fen.strip().split()
    if len(fields) != 6:
        raise ValueError("FEN must have 6 fields")

    placement, active, castling, ep, half, full = fields

    # clear board + sets
    board.board = [[None for _ in range(8)] for _ in range(8)]
    board.white_objects.clear()
    board.black_objects.clear()

    # lazy default factory (avoids import cycles)
    if piece_factory is None:
        def piece_factory(b, sym: str, sq: Square):
            white = sym.isupper()
            s = sym.upper()
            if s == "P":
                from pieces.pawn import Pawn
                return Pawn(b, sq, white)
            elif s == "N":
                from pieces.knight import Knight
                return Knight(b, sq, white)
            elif s == "B":
                from pieces.bishop import Bishop
                return Bishop(b, sq, white)
            elif s == "R":
                from pieces.rook import Rook
                return Rook(b, sq, white)
            elif s == "Q":
                from pieces.queen import Queen
                return Queen(b, sq, white)
            elif s == "K":
                from pieces.king import King
                return King(b, sq, white)
            else:
                raise ValueError(f"Unknown FEN symbol: {sym}")

    # placement
    rows = placement.split("/")
    if len(rows) != 8:
        raise ValueError("FEN piece placement must have 8 ranks")

    for r, rank in enumerate(rows):
        c = 0
        for ch in rank:
            if ch.isdigit():
                c += int(ch)
            else:
                if c >= 8:
                    raise ValueError("Too many files in rank")
                sq = (r, c)
                piece = piece_factory(board, ch, sq)
                board.set_piece(sq, piece)
                (board.white_objects if piece.white else board.black_objects).add(piece)
                if ch == "K":
                    board.white_king = piece
                if ch == "k":
                    board.black_king = piece
                # default times_moved = 0 for all pieces; adjust kings/rooks below
                if hasattr(piece, "times_moved"):
                    piece.times_moved = 0
                c += 1
        if c != 8:
            raise ValueError("Not enough files in rank")

    # active color
    board.white_to_move = (active == "w")

    # castling rights → set times_moved for kings/rooks to align with KQkq
    # Start with "moved", then set back to 0 where rights say so (and piece is on its start square).
    if hasattr(board.white_king, "times_moved"):
        board.white_king.times_moved = 1
    if hasattr(board.black_king, "times_moved"):
        board.black_king.times_moved = 1

    def _rook_at(sq: Square):
        p = board.get_piece(sq)
        return p if (p and p.symbol.lower() == 'r') else None

    wr_h1 = _rook_at((7, 7))
    wr_a1 = _rook_at((7, 0))
    br_h8 = _rook_at((0, 7))
    br_a8 = _rook_at((0, 0))

    # mark rooks moved by default
    for r in (wr_h1, wr_a1, br_h8, br_a8):
        if r and hasattr(r, "times_moved"):
            r.times_moved = 1

    if "K" in castling:
        if board.get_piece((7, 4)) and board.get_piece((7, 4)).symbol == "K":
            board.white_king.times_moved = 0
        if wr_h1:
            wr_h1.times_moved = 0

    if "Q" in castling:
        if board.get_piece((7, 4)) and board.get_piece((7, 4)).symbol == "K":
            board.white_king.times_moved = 0
        if wr_a1:
            wr_a1.times_moved = 0

    if "k" in castling:
        if board.get_piece((0, 4)) and board.get_piece((0, 4)).symbol == "k":
            board.black_king.times_moved = 0
        if br_h8:
            br_h8.times_moved = 0

    if "q" in castling:
        if board.get_piece((0, 4)) and board.get_piece((0, 4)).symbol == "k":
            board.black_king.times_moved = 0
        if br_a8:
            br_a8.times_moved = 0

    # en-passant target
    board.ep_square = None if ep == "-" else alg_to_rc(ep)

    # clocks
    board.half_move_clock = int(fields[4])
    board.full_move_number = int(fields[5])


def fen_key(board) -> str:
    # 4-field, normalized FEN key for threefold repetition:
    # no placement, active color, castling rights, en passant.
    placement_active_castling_ep = to_fen(board, normalize_ep=True).split(" ", 4)[:4]
    return " ".join(placement_active_castling_ep)
