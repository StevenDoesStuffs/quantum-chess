import numpy as np
from qiskit import QuantumCircuit, transpile, quantum_info
from qiskit.providers.aer import AerSimulator
from enum import Enum, auto, unique
import copy

NUM_PIECES = 32
BITS_PER_DIM = 3
BITS_PER_PIECE = BITS_PER_DIM * 2
TOTAL_QUBITS = NUM_PIECES * BITS_PER_PIECE

simulator = AerSimulator(method='matrix_product_state')

# types:
# rook   = 000_ = 0,
# knight = 001_ = 2,
# bishop = 010_ = 4,
# queen  = 0110 = 6,
# king   = 0111 = 7,
# pawn   = 1000 = 8
@unique
class PieceType(Enum):
    ROOK = 0
    KNIGHT = 2
    BISHOP = 4
    QUEEN = 6
    KING = 7
    PAWN = 8

# 5 bits
# CPTTI
# color: white = 0, black = 1
# for pawns:   C = color, P = 0, TTI = index
# for pieces:  C = color, P = 1, TT  = type,  I = index
# for royalty: C = color, P = 1, TTI = type
@unique
class Piece(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return last_values[-1] + 1 if len(last_values) else 0

    WHITE_ROOK_A = auto()
    WHITE_ROOK_B = auto()
    WHITE_KNIGHT_A = auto()
    WHITE_KNIGHT_B = auto()
    WHITE_BISHOP_A = auto()
    WHITE_BISHOP_B = auto()
    WHITE_QUEEN = auto()
    WHITE_KING = auto()
    WHITE_PAWN_0 = auto()
    WHITE_PAWN_1 = auto()
    WHITE_PAWN_2 = auto()
    WHITE_PAWN_3 = auto()
    WHITE_PAWN_4 = auto()
    WHITE_PAWN_5 = auto()
    WHITE_PAWN_6 = auto()
    WHITE_PAWN_7 = auto()
    BLACK_ROOK_A = auto()
    BLACK_ROOK_B = auto()
    BLACK_KNIGHT_A = auto()
    BLACK_KNIGHT_B = auto()
    BLACK_BISHOP_A = auto()
    BLACK_BISHOP_B = auto()
    BLACK_QUEEN = auto()
    BLACK_KING = auto()
    BLACK_PAWN_0 = auto()
    BLACK_PAWN_1 = auto()
    BLACK_PAWN_2 = auto()
    BLACK_PAWN_3 = auto()
    BLACK_PAWN_4 = auto()
    BLACK_PAWN_5 = auto()
    BLACK_PAWN_6 = auto()
    BLACK_PAWN_7 = auto()

    def is_piece(self):
        return (self.value & 0b01000) == 1

    def get_piece_index(self):
        assert self.is_piece()
        return self.value % 2

    def get_pawn_index(self):
        assert not self.is_piece()
        return self.value & 0b00111

    def get_color(self):
        return self.value >> 4

    # returns PTTI with all index bits cleared
    # comparable with PieceType.value
    def get_type(self):
        if self.is_pawn(): return 0b01000
        upper = self.value & 0b00110
        if upper == 6: return upper + self.get_piece_index()
        else: return upper

class Position:
    def __init__(self, file_or_square, rank = None) -> None:
        if rank is None:
            if isinstance(file_or_square, str):
                file_or_square = file_or_square.lower()
                self.value = ((file_or_square[1] - 'a') << BITS_PER_DIM) + (file_or_square[0] - '1')
            else:
                self.value = file_or_square
        else:
            self.value = (file_or_square << BITS_PER_DIM) + rank

    # file, rank
    def pair(self):
        return self.value >> BITS_PER_DIM, self.value & ((1 << BITS_PER_DIM) - 1)

# chess stuff
STARTING_POS = dict()
for color in range(2):
    for type in PieceType:
        if type == PieceType.PAWN:
            for index in range(8):
                piece = Piece((color << 4) + (type.value | index))
                STARTING_POS[piece] = Position(index, 1 if color == 0 else 6)
        else:
            for index in range(2):
                piece = Piece((color << 4) + (type.value | index))
                file = (type.value // 2) if index == 0 else 7 - (type.value // 2)
                rank = 0 if color == 0 else 7
                STARTING_POS[piece] = Position(file, rank)


INITIAL_STATE = 0
for piece in Piece:
    INITIAL_STATE += STARTING_POS[piece].value << (piece.value * BITS_PER_PIECE)

def compute_initial_data():
    circ = QuantumCircuit(TOTAL_QUBITS, TOTAL_QUBITS)
    for i in range(TOTAL_QUBITS):
        if (INITIAL_STATE & (1 << i)) != 0:
            circ.x(i)
    circ.save_matrix_product_state(label='mps')

    result = simulator.run(transpile(circ, simulator)).result()
    return result.data(0)['mps']
INITIAL_DATA = compute_initial_data()

class QuantumChess:
    def __init__(self) -> None:
        self.data = copy.deepcopy(INITIAL_DATA)
        self.alive = {piece: True for piece in Piece}
        # since it's difficult to get an iterable over the nonzero entries
        # of the statevector represented by the mps, we have to keep track
        # of which ones are possibly nonzero
        self.possible = [INITIAL_STATE]
        self.move = 0 # white to move
        self.can_castle = [1, 1]

# data = copy.deepcopy(INITIAL_DATA)
# circ = QuantumCircuit(TOTAL_QUBITS, TOTAL_QUBITS)
# circ.set_matrix_product_state(data)

# print('{:012b}'.format(INITIAL_STATE & ((1 << 12) - 1)))
