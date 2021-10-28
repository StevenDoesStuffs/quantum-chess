from util import *
from classical import *
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

class QuantumChess:
    def __init__(self) -> None:
        self.state = Qubits(TOTAL_QUBITS, INITIAL_STATE)
        self.alive = [True] * NUM_PIECES
        self.move = 0 # white to move
        self.can_castle = [1, 1]

    def flatten(self):
        board = None
        for bv in self.state.statedict:
            if board is None: board = ClassicalBoard(self.alive, bv)
            else: board.merge(ClassicalBoard(self.alive, bv))
        return board

    def get_board(self, index):
        bv = sorted(self.state.statedict)[index] # very slow but who cares
        return ClassicalBoard(self.alive, bv).board

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

mv = MovementValidator()
# print("Is legal: ", mv.legal_move(0, 6, 0, 4, PieceType.PAWN, turn=0, isAttacking=False WRONG
board = QuantumChess()
# board.start_game()
