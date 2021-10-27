from enum import Enum, auto, unique
from quantum import Qubits

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
        # 80% confident this functions as intended, maybe 60%
        return not((self.value & 0b01000) == 0b01000) 

    def is_pawn(self):
        return (self.value & 0b01000)

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

class QuantumChess:
    def __init__(self) -> None:
        self.state = Qubits(TOTAL_QUBITS, INITIAL_STATE)
        self.alive = [True] * NUM_PIECES
        self.move = 0 # white to move
        self.can_castle = [1, 1]

    def flatten(self):
        board = [[None for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        for bv in self.state.statedict:
            for piece in Piece:
                file, rank = Position((bv >> (piece.value * 6)) &
                    ((1 << BITS_PER_PIECE) - 1)).pair()
                assert board[file][rank] is None or \
                    board[file][rank] == piece
                board[file][rank] = piece
        return board

    def printBoard(self):
        flattenedBoard = self.flatten()
        print("    1   2   3   4   5   6   7   8")
        print("  \u250C\u2500\u2500\u2500", end="")
        for i in range(7): print("\u252C\u2500\u2500\u2500", end="")
        print("\u2510")
        for i in range(BOARD_SIZE):
            print(i + 1, "\u2502", end="")
            for j in range(BOARD_SIZE):
                piece = (flattenedBoard[j][7-i])
                if piece != None:
                    piece_code = piece.get_type() + (piece.get_color() << 4)
                    print(" " + pieceType.get(piece_code) + " \u2502", end = "")
                else: print("   \u2502", end = "")
            print("")
            if(i == 7):
                print("  \u2514\u2500\u2500\u2500", end="")
                for i in range(7): print("\u2534\u2500\u2500\u2500", end="")
                print("\u2518")
            else:
                print("  \u251C\u2500\u2500\u2500", end="")
                for i in range(7): print("\u253C\u2500\u2500\u2500", end="")
                print("\u2524")
         
    # Parses user input from <piece_rank> <piece_file> <new_rank> <new_file> to a piece object and board location (piece, rank, file)
    def startGame(self):
        board = self.flatten()
        running = True
        turn = "black"
        while(running):
            if(self.move): 
                self.move = 0
                turn = "black"
            else: 
                self.move = 1
                turn = "white"
            # Lol ^
            piece = None
            while(piece == None):
                self.printBoard()
                print("It is " + turn + "'s turn")
                toParse = input("Use <piece_rank> <piece_file> <new_rank> <new_file> to make your move: ")
                toParse = toParse.split(" ")
                if(len(toParse) != 4 ):
                    print("Invalid input!")
                    continue
                piece = board[int(toParse[0])][int(toParse[1])]

                new_rank = toParse[2]
                new_file = toParse[3]

                if piece == None:
                    print("Invalid piece!")
                    continue

                # At this point we have a piece object (piece) that needs to be moved to a new location (new_rank, new_file)

board = QuantumChess()
board.startGame()
