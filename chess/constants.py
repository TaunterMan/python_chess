# Actual Board
INITIAL_BOARD = [['-'] * 8 for _ in range(8)]
INITIAL_BOARD[0] = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
INITIAL_BOARD[1] = ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p']
INITIAL_BOARD[2] = ['-', '-', '-', '-', '-', '-', '-', '-']
INITIAL_BOARD[3] = ['-', '-', '-', '-', '-', '-', '-', '-']
INITIAL_BOARD[4] = ['-', '-', '-', '-', '-', '-', '-', '-']
INITIAL_BOARD[5] = ['-', '-', '-', '-', '-', '-', '-', '-']
INITIAL_BOARD[6] = ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']
INITIAL_BOARD[7] = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']

# 8x8 of coordinate locations on the board
COORDS = [[''] * 8 for _ in range(8)]
COORDS[7] = ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']
COORDS[6] = ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2']
COORDS[5] = ['a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3']
COORDS[4] = ['a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4']
COORDS[3] = ['a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5']
COORDS[2] = ['a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6']
COORDS[1] = ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7']
COORDS[0] = ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8']

WHITE_PIECES = ['K', 'Q', 'R', 'B', 'N', 'P']
BLACK_PIECES = ['k', 'q', 'r', 'b', 'n', 'p']
