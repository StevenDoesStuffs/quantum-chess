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

def check_row_col(diff_x, diff_y):
    if (diff_x != 0 and diff_y == 0) or (diff_x == 0 and diff_y != 0):
        return True
    return False

def check_diag(diff_x, diff_y):
    if abs(diff_x) == abs(diff_y):
        return True
    return False

def check_knight(diff_x, diff_y):
    if (abs(diff_x) == 2 and abs(diff_y) == 1) or (abs(diff_x) == 2 and abs(diff_y) == 1):
        return True
    return False

def check_king(diff_x, diff_y):
    if abs(diff_x) + abs(diff_y) <= 2:
        if check_diag(diff_x, diff_y) or check_row_col(diff_x, diff_y):
            return True
    return False

def check_pawn(diff_x, diff_y, isAttacking):
    # ADD EN PASSANT LATER

    return False



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

    def classical_check(self, board, unitary):

        return

    # Will check if a move is classically legal solely by movement (DOES NOT CHECK FOR COLLISIONS)
    def legal_move(self, old_pos_x, old_pos_y, new_pos_x, new_pos_y, isAttacking, piece):
        board = self.flatten()
        # piece_type = piece.get_type()
        pt = piece
        diff_x = abs(new_pos_x - old_pos_x)
        diff_y = abs(new_pos_y - old_pos_y)
        
        # no move
        if diff_x == diff_y == 0:
            return False

        check_string = ""
        if (check_row_col(diff_x, diff_y)): check_string += '1'
        else: check_string += '0'
        if (check_diag(diff_x, diff_y)): check_string += '1'
        else: check_string += '0'
        if (check_knight(diff_x, diff_y)): check_string += '1'
        else: check_string += '0'
        if (check_king(diff_x, diff_y)): check_string += '1'
        else: check_string += '0'

        if pt == 0 and check_string == "1000": return True
        elif pt == 2 and check_string == "0010": return True
        elif pt == 4 and check_string == "0100": return True
        elif pt == 6 and check_string == "1100": return True
        elif pt == 7 and check_string[3] == "1": return True
        elif pt == 8 and check_pawn(): return True
        else: return False

    def quantum_move(self, turn):

        return

    def get_board(self, index):
        board = create_board()
        bv = sorted(self.state.statedict)[index] # very slow but who cares
        put_board(board, bv)
        return board

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
print("Is legal: ", mv.legal_move(0, 6, 0, 4, PieceType.PAWN, turn=0, isAttacking=False))
board = QuantumChess()
# board.start_game()
