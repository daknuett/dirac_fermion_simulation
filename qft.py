from pyqcs import (X, H, S, R, CX
                   , State
                   , list_to_circuit
                   , sample, compute_amplitudes)

def CRk(act, control, k):
    angle = 2*np.pi / 2**(k)
    return R(act, angle/2) | CX(act, control) | (R(control, angle/2) | R(act, -angle/2)) | CX(act, control)
def cascading_crk(i, bits):
    circuit_list = [CRk(bits[i], c, j+2) for j,c in reversed(list(enumerate(bits[i + 1:])))]
    return list_to_circuit(circuit_list)

def SWAP(i, j):
    return CX(i, j) | CX(j, i) | CX(i, j)

def QFT(bits):
    if(isinstance(bits, int)):
        bits = [i for i in range(bits.bit_length() + 1) if bits & (1 << i)]
    if(not isinstance(bits, (list, tuple))):
        raise TypeError("bits must be either int, list or tuple")
        
    reversed_bits = list(reversed(bits))
    
    circuit = [H(qbit) | cascading_crk(i, reversed_bits) for i,qbit in enumerate(reversed_bits)]
    circuit = list_to_circuit(circuit)
    
    
    nbits = len(bits)
    swap_bits = list_to_circuit([SWAP(bits[i], bits[nbits - i - 1]) for i in range(nbits//2)])
    

    return circuit | swap_bits

