from enum import Enum, auto, unique

BOARD_SIZE = 8
NUM_PIECES = 32
BITS_PER_DIM = 3
BITS_PER_PIECE = BITS_PER_DIM * 2
TOTAL_QUBITS = NUM_PIECES * BITS_PER_PIECE

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

@unique
class Color(Enum):
    WHITE = 0b00000
    BLACK = 0b10000

pieceType = {
    0 : "\u2656", ## White Rook
    2 : "\u2658", ## White Knight
    4 : "\u2657", ## White Bishop
    6 : "\u2655", ## White Queen
    7 : "\u2654", ## White King
    8 : "\u2659", # White Pawn

    16 : "\u265C", ## Black Rook
    18 : "\u265E", ## Black Knight
    20 : "\u265D", ## Black Bishop
    22 : "\u265B", ## Black Queen
    23 : "\u265A", ## Black King
    24 : "\u265F", ## Black Pawn (Note: Looks funky on certain specs)

    None : " "
}

# 5 bits
# CPTTI
# color: white = 0, black = 1
# for pawns:   C = color, P = 1, TTI = index
# for pieces:  C = color, P = 0, TT  = type,  I = index
# for royalty: C = color, P = 0, TTI = type
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

    def is_pawn(self):
        return bool(self.value & 0b01000)

    def is_piece(self):
        return not self.is_pawn()

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
                self.value = (
                    (ord(file_or_square[0]) - ord('a')) << BITS_PER_DIM) + \
                    (ord(file_or_square[1]) - ord('1'))
            else: self.value = file_or_square
        else: self.value = (file_or_square << BITS_PER_DIM) + rank

    def __repr__(self) -> str:
        file, rank = self.pair()
        return chr(ord('a') + file) + chr(ord('1') + rank)

    # file, rank
    def pair(self):
        return self.value >> BITS_PER_DIM, self.value & ((1 << BITS_PER_DIM) - 1)
        
# Movement Validation
def check_axis(diff_x, diff_y):
    return (diff_x and not diff_y) or (not diff_x and diff_y)

def check_diag(diff_x, diff_y):
    return abs(diff_x) == abs(diff_y)

def check_knight(diff_x, diff_y):
    return (abs(diff_x) == 2 and abs(diff_y) == 1) or (abs(diff_x) == 2 and abs(diff_y) == 1)

def check_queen(diff_x, diff_y):
    return check_axis(diff_x, diff_y) or check_diag(diff_x, diff_y)

def check_king(diff_x, diff_y):
    if abs(diff_x) + abs(diff_y) <= 2:
        return check_diag(diff_x, diff_y) or check_row_col(diff_x, diff_y)

def check_pawn(diff_x, diff_y, turn, isAttacking, old_y):
    if turn:
        if isAttacking: return (diff_y == -1) and (abs(diff_x) == 1)
        elif old_y == 1 and diff_y == -2: return True  # EN PASSANT
        else: return (not diff_x and diff_y == -1)
        

    else:
        if isAttacking: return (diff_y == 1) and (abs(diff_x) == 1)
        elif old_y == 7 and diff_y == 2: return True # EN PASSANT
        else: return (not diff_x and diff_y == 1)

    

# Checks for valid classical move (DOES NOT CHECK FOR COLLISIONS)
def legal_move(old_pos_x, old_pos_y, new_pos_x, new_pos_y, piece, turn, isAttacking=False):
    pt = piece
    diff_x = abs(new_pos_x - old_pos_x)
    diff_y = abs(new_pos_y - old_pos_y)

    # no move
    if diff_x == diff_y == 0:
            return False

    if pt == PieceType.ROOK: return check_axis(diff_x, diff_y)
    elif pt == PieceType.KNIGHT: return check_knight(diff_x, diff_y)
    elif pt == PieceType.BISHOP: return check_diag(diff_x, diff_y)
    elif pt == PieceType.QUEEN: return check_queen(diff_x, diff_y)
    elif pt == PieceType.KING: return check_king(diff_x, diff_y)
    elif pt == PieceType.PAWN: return check_pawn(diff_x, diff_y, turn, isAttacking, old_pos_y)
    else: return False # Invalid piece
