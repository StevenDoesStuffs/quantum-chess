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



    def legal_move(old_pos_x, old_pos_y, new_pos_x, new_pos_y, isAttacking, piece):
        diff_x = new_pos_x - old_pos_x
        diff_y = new_pos_y - old_pos_y
        # For horizontal movement
        if diff_x == diff_y

        return False

    def printBoard(self):
        flattenedBoard = self.flatten()
    def get_board(self, index):
        board = create_board()
        bv = sorted(self.state.comp)[index] # very slow but who cares
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
            if(self.move):
                self.move = 0
                turn = "black"
            else:
                self.move = 1
                turn = "white"
            # Lol ^
            piece = None
            while(piece == None):
                # board = self.flatten()
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
board.start_game()
