from util import *
from quantum import Qubits

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

def put_board(board, bv):
    for piece in Piece:
        file, rank = Position((bv >> (piece.value * 6)) &
            ((1 << BITS_PER_PIECE) - 1)).pair()
        assert board[file][rank] is None or \
            board[file][rank] == piece
        board[file][rank] = piece
    return board

def create_board():
    return [[None for _i in range(BOARD_SIZE)] for _j in range(BOARD_SIZE)]

class QuantumChess:
    def __init__(self) -> None:
        self.state = Qubits(TOTAL_QUBITS, INITIAL_STATE)
        self.alive = [True] * NUM_PIECES
        self.move = 0 # white to move
        self.can_castle = [1, 1]

    def flatten(self):
        board = create_board()
        for bv in self.state.statedict:
            put_board(board, bv)
        return board

    def get_board(self, index):
        board = create_board()
        bv = sorted(self.state.statedict)[index] # very slow but who cares
        put_board(board, bv)
        return board;

    def print_board(self, board):
        print("    1   2   3   4   5   6   7   8")
        print("  \u250C\u2500\u2500\u2500", end="")
        for i in range(7): print("\u252C\u2500\u2500\u2500", end="")
        print("\u2510")
        for i in range(BOARD_SIZE):
            print(i + 1, "\u2502", end="")
            for j in range(BOARD_SIZE):
                piece = (board[j][7-i])
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
    def start_game(self):
        board = self.flatten()
        running = True
        turn = "black"
        while(running):
            if(self.move): turn = "black"
            else: turn = "white"
            self.move = not(self.move)
            display_board = None
            while(display_board == None):
                available = len(self.state.statedict)
                display_board = int(input("Choose board (boards available " + str(available) + "): "))
                if(display_board not in range(available)):
                    print("Invalid board selected")
                    display_board = None
            display_board = self.get_board(display_board)
            self.print_board(display_board)
            # Continue game


board = QuantumChess()
board.start_game()
