from math import sqrt
import random
from collections import defaultdict
from scipy import sparse
from util import *

THRESHOLD = 1e-5

def bit(num, i):
    return int((num & (1 << i)) != 0)

class Qubits:
    def __init__(self, n, val):
        self.n = n
        self.statedict = defaultdict(complex)
        self.statedict[val] = complex(1)

    def append(self):
        self.n += 1
        return self.n - 1

    def cx(self, ctrl, target):
        new = defaultdict(complex)
        for bv in self.statedict:
            index = bv if bit(bv, ctrl) == 0 else bv ^ (1 << target)
            new[index] += self.statedict[bv]
        self.statedict = new
        self.clean()

    def mcmu(self, pattern, perm, controls, targets):
        new = defaultdict(complex)
        bitmask = sum((1 << target for target in targets))
        def tb(val_t):
            val_b = 0
            for i in range(len(targets)):
                if bit(val_t, i) == 1:
                    val_b += (1 << targets[i])
            return val_b

        perm = {tb(from_t): {tb(to_t): to_coeff \
                for to_t, to_coeff in to.items()} \
            for from_t, to in perm.items()}

        for bv in self.statedict:
            for i in range(len(controls)):
                if bit(bv, controls[i]) != bit(pattern, i):
                    new[bv] += self.statedict[bv]
                    break
            else:
                cleared = bv & ~bitmask
                val_t = bv & bitmask
                if val_t not in perm: continue
                for to_b in perm[val_t]:
                    result_b = cleared + to_b
                    new[result_b] += self.statedict[bv] * \
                        perm[val_t][to_b]
        self.statedict = new
        self.clean()

    def measure(self, indices):
        result = 0
        for i in range(len(indices)):
            index = indices[i]
            p1 = 0
            for bv in self.statedict:
                if bit(bv, index) != 0:
                    p1 += abs(self.statedict[bv]) ** 2
            is_one = random.uniform(0, 1) <= p1
            for bv in self.statedict:
                if bit(bv, index) != int(is_one):
                    self.statedict[bv] = 0
            self.normalize()
            if is_one: result += 1 << i
        return result

    def normalize(self):
        mag = 0
        for bv in self.statedict:
            mag += abs(self.statedict[bv]) ** 2
        mag = sqrt(mag)
        for bv in self.statedict:
            self.statedict[bv] /= sqrt(mag)

    def clean(self):
        self.statedict = defaultdict(complex, filter(
            lambda x: abs(x[1]) >= THRESHOLD,
            self.statedict.items()))
        self.normalize()

def numeric_map(pos_map):
    return {
        source.value: {
            target.value: pos_map[source][target] \
                for target in pos_map[source]
        } for source in pos_map
    }


def check_unitary(numeric_map):
    matrix = sparse.identity(BOARD_SIZE ** 2, dtype=complex, format='dok')
    for source in numeric_map: # source = col, target = row
        matrix[source, source] = 0
    for source in numeric_map:
        for target in numeric_map[source]:
            matrix[target, source] = numeric_map[source][target]
    matrix = matrix.conjtransp().dot(matrix)
    print(matrix)
    # matrix -= sparse.identity(BOARD_SIZE ** 2, dtype=complex, format='dok')
    # sum = 0
    # for elem in matrix.keys():
    #     sum += abs(matrix[elem]) ** 2
    # return sqrt(sum)
