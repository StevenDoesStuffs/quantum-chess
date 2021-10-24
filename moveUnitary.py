import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
import numpy as np

#Other File imports
from utility import *

# Movement unitaries will require 3 auxillary qubits in order to move a piece without destroying data
def add(qc, qs_input, qs_output):
    qft(qc, len(qs_output))
    # qc.barrier()

    #phase application
    for i in range(len(qs_output)):
        for j in range(len(qs_input) - i):
            qc.cu1(2*np.pi / (2**((len(qs_input) - i - j - 1))), qs_input[j], qs_output[i])
            # qc.barrier()
    qft_inv(qc, qs_output)

def subtract(qc, qs_input, qs_output):
    qft(qc, len(qs_output))
    # qc.barrier()

    #phase application
    for i in range(len(qs_output)):
        for j in range(len(qs_input) - i):
            qc.cu1(-2*np.pi / (2**((len(qs_input) - i - j - 1))), qs_input[j], qs_output[i])
            # qc.barrier()

    qft_inv(qc, qs_output)

def moveY(qpiece, dist):
    
    return

def moveX(qpiece, dist):
    
    return
