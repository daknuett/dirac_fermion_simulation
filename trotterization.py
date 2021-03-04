from pyqcs import (X, H, S, R, CX
                   , list_to_circuit)

from qft import QFT
from circuits import CRX, CRY, RZ, C5R, C5X

def Ttrot(qbits_phi, qbits_px, qbits_py, dt, c, momentum_omegas):
    circuit_list = []
    for qb_phi in qbits_phi:
        for j, qb_px in enumerate(qbits_px):
            circuit_list.append(CRX(qb_phi, qb_px, dt*c**2*momentum_omegas[j]))
        for j, qb_py in enumerate(qbits_py):
            circuit_list.append(CRY(qb_phi, qb_py, dt*c**2*momentum_omegas[j]))
    return list_to_circuit(circuit_list)

def TtrotLandau(qbits_phi, qbits_px, qbits_py, dt, c, B, momentum_omegas):
    circuit_list = []
    for qb_phi in qbits_phi:
        circuit_list.append(QFT(qbits_px))       
        for j, qb_px in enumerate(qbits_px):
            circuit_list.append(CRY(qb_phi, qb_px, dt*c*B*momentum_omegas[j]))
        circuit_list.append(QFT(qbits_px).get_dagger())
            
        circuit_list.append(QFT(qbits_py))
        for j, qb_py in enumerate(qbits_py):
            circuit_list.append(CRX(qb_phi, qb_py, -dt*c*B*momentum_omegas[j]))
        circuit_list.append(QFT(qbits_py).get_dagger())
        
    return list_to_circuit(circuit_list)

def Ttrot_potential(qbits_px, ancillas, dt, V0):
    return ( list_to_circuit([H(i) for i in qbits_px[-5:]])
            | C5R(qbits_px[0], qbits_px[-5:], ancillas, dt*V0/2)
            | C5X(qbits_px[0], qbits_px[-5:], ancillas)
            | C5R(qbits_px[0], qbits_px[-5:], ancillas, dt*V0/2)
            | C5X(qbits_px[0], qbits_px[-5:], ancillas)
            | list_to_circuit([H(i) for i in qbits_px[-5:]])
           )
    
