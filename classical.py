from util import *

class MovementValidator:
    def __check_axis(diff_x, diff_y):
        return (diff_x and not diff_y) or (not diff_x and diff_y)

    def __check_diag(diff_x, diff_y):
        return abs(diff_x) == abs(diff_y)

    def __check_knight(diff_x, diff_y):
        return (abs(diff_x) == 2 and abs(diff_y) == 1) or (abs(diff_x) == 2 and abs(diff_y) == 1)

    def __check_queen(self, diff_x, diff_y):
        return self.__check_axis(diff_x, diff_y) or self.__check_diag(diff_x, diff_y)

    def __check_king(self, diff_x, diff_y):
        if abs(diff_x) + abs(diff_y) <= 2:
            return self.__check_diag(diff_x, diff_y) or self.__check_row_col(diff_x, diff_y)

    def __check_pawn(self, diff_x, diff_y, turn, isAttacking, old_y):
        if turn:
            if isAttacking: return (diff_y == -1) and (abs(diff_x) == 1)
            elif old_y == 1 and diff_y == -2 and not diff_x: return True  # EN PASSANT
            else: return (not diff_x and diff_y == -1)
            

        else:
            if isAttacking: return (diff_y == 1) and (abs(diff_x) == 1)
            elif old_y == 7 and diff_y == 2 and not diff_x: return True # EN PASSANT
            else: return (not diff_x and diff_y == 1)

    # Checks for valid classical move (DOES NOT CHECK FOR COLLISIONS)
    def legal_move(self, old_pos, new_pos, piece, isAttacking=False):
        pt = piece.get_type()
        diff_x = abs(new_pos[0] - old_pos[0])
        diff_y = abs(new_pos[1] - old_pos[1])
        if diff_x == diff_y == 0:
                return False
        if pt == PieceType.ROOK: return self.__check_axis(diff_x, diff_y)
        elif pt == PieceType.KNIGHT: return self.__check_knight(diff_x, diff_y)
        elif pt == PieceType.BISHOP: return self.__check_diag(diff_x, diff_y)
        elif pt == PieceType.QUEEN: return self.__check_queen(diff_x, diff_y)
        elif pt == PieceType.KING: return self.__check_king(diff_x, diff_y)
        elif pt == PieceType.PAWN: return self.__check_pawn(diff_x, diff_y, piece.get_color(), isAttacking, old_pos[1])
        else: return False # Invalid piece

    def collision_check(self, cboard, piece, old_pos, new_pos):
        diff_x = abs(new_pos[0] - old_pos[0])
        diff_y = abs(new_pos[1] - old_pos[1])
        if piece.get_type() != 2:
            return
        return

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

def print_board(board):
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