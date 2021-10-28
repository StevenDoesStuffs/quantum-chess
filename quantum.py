from numpy.lib.arraysetops import isin
from scipy import sparse
from simulator import THRESHOLD
from util import *

def numeric_map(pos_map):
    return {
        source.value: {
            target.value: pos_map[source][target] \
                for target in pos_map[source]
        } for source in pos_map
    }

def check_unitary(numeric_map):
    matrix = sparse.identity(BOARD_SIZE ** 2, dtype=complex, format='dok')
    for source in numeric_map: # source = col, target = row
        matrix[source, source] = 0
    for source in numeric_map:
        for target in numeric_map[source]:
            matrix[target, source] = numeric_map[source][target]
    matrix = matrix.conjtransp().dot(matrix)
    matrix -= sparse.identity(BOARD_SIZE ** 2, dtype=complex)

    sum = 0
    rows, cols = matrix.nonzero()
    for r, c in zip(list(rows), list(cols)):
        sum += abs(matrix[r, c]) ** 2
    return sum < THRESHOLD

# TURN: (Piece, MOVE)
# MOVE: MAP | IF
# COND: (Piece, Position)
# IF: (COND, TURN, TURN) # first is true, second is false
# MAP: dict(Position, dict(Position, complex))
# move: condition, turn, turn
def find_move(move, cboard):
    if isinstance(move, dict):
        return move
    else:
        condition, turn_true, turn_false = move
        piece, position = condition
        file, rank = position.pair()
        if cboard[file][rank] == piece:
            return find_move(turn_true, cboard)
        else:
            return find_move(turn_false, cboard)

def quantum_move(board, turn, mv):
    piece, move = turn
    
    if isinstance(move, dict):
        mv.legal_move(piece[0].pair(), piece[1].pair(), )

    return

def quantum_check(board, move):
    for cboard in board.



    return