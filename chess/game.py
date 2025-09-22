from __future__ import annotations

from chess.board import Board
from chess.san import parse_san_to_move

FILES = "abcdefgh"


def print_board(board: Board) -> None:
    # row 0 is rank 8; row 7 is rank 1
    for r in range(8):
        rank = 8 - r
        row_syms = []
        for c in range(8):
            p = board.get_piece((r, c))
            row_syms.append(p.symbol if p else ".")
        print(f"{rank}  " + " ".join(row_syms))
    print("   " + " ".join(FILES))


def side_str(board: Board) -> str:
    return "White" if board.white_to_move else "Black"


def main() -> None:
    board = Board()  # initialize in the starting position
    print_board(board)

    while True:
        # game end checks
        if board.checkmate:
            print(f"Checkmate! {'Black' if board.white_to_move else 'White'} wins.")
            break
        if board.stalemate:
            print("Stalemate.")
            break
        if board.check_insufficient_material():
            print("Insufficient Material.")
            break
        if board.check_fifty_move_rule():
            print("Fifty-move rule draw.")
            break
        if board.check_threefold_repetition():
            print("Threefold repetition draw.")
            break

        # print status
        turn = side_str(board)
        in_check = board.check(board.white_to_move)
        print(
            f"{turn} to move{' (check)' if in_check else ''}. Enter SAN (e.g., e4, Nf3, O-O), "
            f"or 'undo', 'print', 'quit'.")

        s = input("> ").strip()

        # simple commands
        if s.lower() in ("q", "quit", "exit"):
            print("Game ended by user.")
            break
        if s.lower() in ("p", "print", "board"):
            print_board(board)
            continue
        if s.lower() in ("u", "undo"):
            try:
                board.unmake_move()
            except Exception as e:
                print(f"Nothing to undo ({e}).")
            else:
                print_board(board)
            continue
        if not s:
            continue

        # try SAN
        try:
            mv = parse_san_to_move(board, s)
        except ValueError as e:
            print(f"Invalid move: {e}")
            continue

        # apply and show
        try:
            board.make_move(mv)
        except Exception as e:
            print(f"Could not make move: {e}")
            continue

        print_board(board)


if __name__ == "__main__":
    main()
