from pyqcs import X, H, State, list_to_circuit
from .circuits import RZ
from .log_time import log_time


def prepare_momentum_eigenstate(nqbits, qbits_px, qbits_py, qbits_phi
                                , px_init, py_init, phi_init, antifermion):
    with log_time(__name__, "prepare_momentum_eigenstate"):
        state = State.new_zero_state(nqbits)

        circuit_px_init = [X(q) for i,q in enumerate(qbits_px) if px_init & (1 << i)]
        circuit_px_init = list_to_circuit(circuit_px_init)
        circuit_py_init = [X(q) for i,q in enumerate(qbits_py) if py_init & (1 << i)]
        circuit_py_init = list_to_circuit(circuit_py_init)

        if(not antifermion):
            state = (H(qbits_phi[0])
                     | RZ(qbits_phi[0], phi_init)
                     | circuit_px_init | circuit_py_init) * state
        else:
            state = (X(qbits_phi[0])
                     | H(qbits_phi[0])
                     | RZ(qbits_phi[0], phi_init)
                     | circuit_px_init | circuit_py_init) * state
    return state
