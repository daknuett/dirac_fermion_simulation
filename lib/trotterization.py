from pyqcs import X , list_to_circuit

from .qft import QFT
from .circuits import CRX, CRY, C5R, C5X, CRI
from .controlled_gate import ncontrolled


def Ttrot(qbits_phi, qbits_px, qbits_py, dt, c, momentum_omegas):
    circuit_list = []
    for qb_phi in qbits_phi:
        for j, qb_px in enumerate(qbits_px):
            circuit_list.append(CRX(qb_phi, qb_px, -dt * c**2 * momentum_omegas[j]))
        for j, qb_py in enumerate(qbits_py):
            circuit_list.append(CRY(qb_phi, qb_py, -dt * c**2 * momentum_omegas[j]))
    return list_to_circuit(circuit_list)


def TtrotLandau(qbits_phi, qbits_px, qbits_py, dt, c, B, momentum_omegas):
    circuit_list = []
    for qb_phi in qbits_phi:
        circuit_list.append(QFT(qbits_px).get_dagger())
        for j, qb_px in enumerate(qbits_px):
            circuit_list.append(CRY(qb_phi, qb_px, -dt * c * B * momentum_omegas[j]))
        circuit_list.append(QFT(qbits_px).get_dagger())

        circuit_list.append(QFT(qbits_py))
        for j, qb_py in enumerate(qbits_py):
            circuit_list.append(CRX(qb_phi, qb_py, dt * c * B * momentum_omegas[j]))
        circuit_list.append(QFT(qbits_py))

    return list_to_circuit(circuit_list)


def Ttrot_potential(qbits_px, ancillas, dt, V0):
    return (QFT(qbits_px).get_dagger()
            | list_to_circuit([X(i) for i in qbits_px[-5:]])
            | C5R(qbits_px[0], qbits_px[-5:], ancillas, -dt * V0 / 2)
            | C5X(qbits_px[0], qbits_px[-5:], ancillas)
            | C5R(qbits_px[0], qbits_px[-5:], ancillas, -dt * V0 / 2)
            | C5X(qbits_px[0], qbits_px[-5:], ancillas)
            | list_to_circuit([X(i) for i in qbits_px[-5:]])
            | QFT(qbits_px)
           )


def Ttrot_potential_optimized_8qbits(qbits_px, ancillas, dt, V0):
    return (QFT(qbits_px).get_dagger()
            | list_to_circuit([X(i) for i in qbits_px[-6:]])
            | ncontrolled(qbits_px[0], CRI, ancillas, qbits_px[-6:], -dt * V0 / 2)
            | list_to_circuit([X(i) for i in qbits_px[-6:]])
            | QFT(qbits_px))
