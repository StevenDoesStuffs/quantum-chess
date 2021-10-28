from util import *

class MovementValidator:
    def __check_axis(diff_x, diff_y):
        return (diff_x and not diff_y) or (not diff_x and diff_y)

    def __check_diag(diff_x, diff_y):
        return abs(diff_x) == abs(diff_y)

    def __check_knight(diff_x, diff_y):
        return (abs(diff_x) == 2 and abs(diff_y) == 1) or (abs(diff_x) == 2 and abs(diff_y) == 1)

    def __check_queen(diff_x, diff_y):
        return check_axis(diff_x, diff_y) or check_diag(diff_x, diff_y)

    def __check_king(diff_x, diff_y):
        if abs(diff_x) + abs(diff_y) <= 2:
            return check_diag(diff_x, diff_y) or check_row_col(diff_x, diff_y)

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
    def legal_move(self, old_pos_x, old_pos_y, new_pos_x, new_pos_y, piece, turn, isAttacking=False):
        pt = piece
        diff_x = abs(new_pos_x - old_pos_x)
        diff_y = abs(new_pos_y - old_pos_y)

        # no move
        if diff_x == diff_y == 0:
                return False

        if pt == PieceType.ROOK: return self.__check_axis(diff_x, diff_y)
        elif pt == PieceType.KNIGHT: return self.__check_knight(diff_x, diff_y)
        elif pt == PieceType.BISHOP: return self.__check_diag(diff_x, diff_y)
        elif pt == PieceType.QUEEN: return self.__check_queen(diff_x, diff_y)
        elif pt == PieceType.KING: return self.__check_king(diff_x, diff_y)
        elif pt == PieceType.PAWN: return self.__check_pawn(diff_x, diff_y, turn, isAttacking, old_pos_y)
        else: return False # Invalid piece
        