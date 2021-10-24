import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
import numpy as np

def cR(qc, n):
    if n == 0:
        return
    qc.h(n-1)
    for i in range(n - 1):
        qc.cu1(2*np.pi/2**(n - i), i, n-1)
    cR(qc, n - 1)

def qft(qc,n): 
    cR(qc, n)
    qc.barrier()

    for i in range(n // 2):
        qc.swap(i, n - i - 1)
    qc.barrier()

    return qc

def qft_inv(qc, q):
    
    n = len(q)
    
    for l in range(n//2):
        qc.swap(q[l], q[n-1-l])
    
    for j in range(n):
        for k in range(j):
            qc.cu1(-2*np.pi*2**(-(j-k+1)), q[k], q[j])
        qc.h(q[j])



