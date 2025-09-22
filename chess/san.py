
import re

FILES = "abcdefgh"

def alg_to_rc(alg: str) -> tuple[int, int]:
    col = ord(alg[0]) - ord('a')
    row = 8 - int(alg[1])
    return (row, col)

def rc_to_alg(rc: tuple[int, int]) -> str:
    row, col = rc
    file_ch = chr(ord('a') + col)
    rank_ch = str(8 - row)
    return f"{file_ch}{rank_ch}"

SAN = re.compile(r"""
^ \s*
(?:
    (?P<castle>O-O(?:-O)?|0-0(?:-0)?) |
    (?P<piece>[KQRBN])?
    (?P<disamb>[a-h][1-8]|[a-h]|[1-8])?
    (?P<capture>x)?
    (?P<dst>[a-h][1-8])
    (?:=(?P<promo>[QRBN]))?
    (?P<check>[+#])?
)
\s*$
""", re.VERBOSE)

def parse_san_to_move(board, san: str):
    san = san.strip()
    m = SAN.match(san)
    if not m:
        raise ValueError(f"Not SAN: {san}")

    # Castling
    if m.group("castle"):
        ks = m.group("castle") in ("O-O", "0-0")
        for mv in board.legal_moves():                  # list[Move]
            if (ks and mv.castle_ks) or ((not ks) and mv.castle_qs):
                return mv
        raise ValueError("Castling move not legal here")

    # Normal move
    piece_letter = m.group("piece")  # None => pawn
    disamb = m.group("disamb") or ""
    wants_capture = m.group("capture") is not None
    dst = alg_to_rc(m.group("dst"))
    promo_letter = m.group("promo")  # only relevant for pawns

    # Build constraints
    def is_piece_type(mv):
        # Normalize to uppercase for type compare
        t = mv.piece.upper()
        if not piece_letter:
            return t == 'P'
        return t == piece_letter

    def matches_capture(mv):
        return mv.capture == wants_capture

    def matches_promo(mv):
        if promo_letter is None:
            return mv.promotion is None
        # normalize promo to uppercase for compare
        return (mv.promotion or '').upper() == promo_letter

    def matches_disamb(mv):
        if not disamb:
            return True
        r, c = mv.source
        # file (a-h), rank (1-8), or both (e.g., 'e' or '4' or 'e4')
        f_ok = True
        r_ok = True
        if len(disamb) == 2:
            f_ok = (c == FILES.index(disamb[0]))
            r_ok = (r == 8 - int(disamb[1]))
        elif disamb.isalpha():
            f_ok = (c == FILES.index(disamb))
        else:
            r_ok = (r == 8 - int(disamb))
        return f_ok and r_ok

    candidates = [
        mv for mv in board.legal_moves()
        if mv.destination == dst
        and is_piece_type(mv)
        and matches_capture(mv)
        and matches_promo(mv)
        and matches_disamb(mv)
    ]

    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) == 0:
        raise ValueError(f"No legal move matches {san}")
    raise ValueError(f"Ambiguous SAN {san}: {len(candidates)} candidates")