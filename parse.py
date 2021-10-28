from util import *

class ParseError(Exception):
    def __init__(self, index) -> None:
        super().__init__()
        self.index = index

def optional(func):
    try:
        return func()
    except (ParseError, IndexError, ValueError):
        return False

def enforce(cond, index):
    if not cond: raise ParseError(index)

def read_piece(input, index):
    if input[index] == 'P':
        val = int(input[index + 1])
        if val == 0 or val > 8: raise ParseError(index)
        val -= 1
        return PieceType.PAWN + val
    elif not (input[]):
        val = int(input[index + 1])
        if val == 0 or val > 2: raise ParseError(index)
        val -= 1



def read_str(input, index, string):
    if input[index:index + len(string)] == string:
        return index + len(string), True
    else: raise ParseError(index)

def read_turn(input, index):
    piece = parse_piece()


