import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute, MatrixOperator
import numpy as np

import numpy as np
from qiskit import QuantumCircuit, transpile, quantum_info
from qiskit.providers.aer import AerSimulator

def coefficient(data, i) -> complex:
    mps, lambdas = data
    matrix = mps[0][i % 2]
    for j in range(1, len(mps)):
        for k in range(len(lambdas[j - 1])):
            matrix[:, k] *= lambdas[j - 1][k]
        matrix = np.matmul(matrix, mps[j][(i >> j) % 2])
    return matrix[0][0]
