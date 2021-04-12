from .trotterization import Ttrot, Ttrot_potential, Ttrot_potential_optimized_8qbits
from .log_time import log_time


def simulate_free_case(state, qbits_px, qbits_py, qbits_phi, c, dt, momentum_omegas, t):
    with log_time(__name__, "simulate_free_case"):
        n = int(t / dt)
        circuit = Ttrot(qbits_phi, qbits_px, qbits_py, dt, c, momentum_omegas)
        for _ in range(n):
            state = circuit * state
    return state


def simulate_with_potential(state, qbits_px, qbits_py, qbits_phi, ancillas, c, dt, V0, momentum_omegas, t):
    with log_time(__name__, "simulate_with_potential"):
        n = int(t / dt)
        circuit = (Ttrot(qbits_phi, qbits_px, qbits_py, dt, c, momentum_omegas)
                    | Ttrot_potential(qbits_px, ancillas, dt, V0))
        for _ in range(n):
            state = circuit * state
    return state


def simulate_with_potential_optimized(state, qbits_px, qbits_py, qbits_phi, ancillas, c, dt, V0, momentum_omegas, t):
    with log_time(__name__, "simulate_with_potential"):
        n = int(t / dt)
        circuit = (Ttrot(qbits_phi, qbits_px, qbits_py, dt, c, momentum_omegas)
                    | Ttrot_potential_optimized_8qbits(qbits_px, ancillas, dt, V0))
        for _ in range(n):
            state = circuit * state
    return state
