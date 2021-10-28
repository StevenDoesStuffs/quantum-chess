from util import *
import math

class ClassicalBoard:
    def __init__(self, alive, bv) -> None:
        self.bv = bv
        self.board = [[None for _i in range(BOARD_SIZE)] for _j in range(BOARD_SIZE)]
        self.put_board(bv)
        self.alive = alive
        pass

    def merge(self, other):
        assert self.alive == other.alive
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                assert self.board[i][j] is None or \
                    self.board[i][j] == other[i][j]
                self.board[i][j] = other[i][j]

    def put_board(self):
        for piece in Piece:
            if not self.alive[piece.value]: continue

            file, rank = self.get_pos(piece)
            self.board[file][rank] = piece

    def get_pos(self, piece):
        if not self.alive[piece.value]: return None
        else: return Position((self.bv >>
            (piece.value * 6)) & ((1 << BITS_PER_PIECE) - 1))

    def get_piece(self, pos):
        return self.board[pos]


class MovementValidator:

    def __init__(self, cboard, piece) -> None:
        self.board = cboard
        self.piece = piece

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

    def __check_pawn(self, diff_x, diff_y):
        old_x, old_y = self.board.get_pos(self.piece)
        is_attacking = self.board.get_piece(
            Position(old_x + diff_x, old_y + diff_y)) is not None

        if self.piece.get_color() == Color.WHITE.value:
            if is_attacking: return (diff_y == -1) and (abs(diff_x) == 1)
            elif self.board.get_pos(self.piece)[1] == 1 \
                and diff_y == -2 and not diff_x: return True
            else: return not diff_x and diff_y == -1
        else:
            if is_attacking: return (diff_y == 1) and (abs(diff_x) == 1)
            elif self.board.get_pos(self.piece)[1] == 6 \
                and diff_y == 2 and not diff_x: return True
            else: return not diff_x and diff_y == 1

    def __diff(self, new_pos):
        diff_x, diff_y = new_pos
        old_x, old_y = self.board.get_pos(self.piece)
        diff_x -= old_x
        diff_y -= old_y
        return diff_x, diff_y

    # Checks for valid classical move (DOES NOT CHECK FOR COLLISIONS)
    def legal_move(self, new_pos):
        pt = self.piece.get_type()
        diff_x, diff_y = self.__diff(new_pos)

        if diff_x == diff_y == 0: return False
        if pt == PieceType.ROOK: return self.__check_axis(diff_x, diff_y)
        elif pt == PieceType.KNIGHT: return self.__check_knight(diff_x, diff_y)
        elif pt == PieceType.BISHOP: return self.__check_diag(diff_x, diff_y)
        elif pt == PieceType.QUEEN: return self.__check_queen(diff_x, diff_y)
        elif pt == PieceType.KING: return self.__check_king(diff_x, diff_y)
        elif pt == PieceType.PAWN: return self.__check_pawn(diff_x, diff_y)
        else: return False # Invalid piece

    def collision_check(self, new_pos):
        diff_x, diff_y = self.__diff(new_pos)
        pos = self.board.get_pos(self.piece)

        if self.piece.get_type() == PieceType.KNIGHT.value:
            return False

        for _i in range(1, max(diff_x, diff_y)):
            if diff_x != 0: pos[0] += math.copysign(1, diff_x)
            if diff_y != 0: pos[1] += math.copysign(1, diff_y)
            if self.board.get_piece(pos) is not None: return True
        return False

    def get_eaten(self, new_pos):
        return self.board.get_piece(new_pos)



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
