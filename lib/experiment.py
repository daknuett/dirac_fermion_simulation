import numpy as np

from .state_preparation import prepare_momentum_eigenstate
from .simulation import simulate_free_case, simulate_with_potential, simulate_with_potential_optimized
from .readout import compute_all_amplitudes, compute_all_amplitudes_no_conversion
from .log_time import log_time


def experiment_free_case_time_evolution(qbits_px, qbits_py, qbits_phi, px_init, py_init, phi_init, antifermion, c, dt, N, momentum_omegas, eps, t):
    with log_time(__name__, "experiment_free_case_time_evolution"):
        state = prepare_momentum_eigenstate(len(qbits_px) + len(qbits_py) + len(qbits_phi)
                                            , qbits_px, qbits_py, qbits_phi
                                            , px_init, py_init, phi_init, antifermion)
        state = simulate_free_case(state, qbits_px, qbits_py, qbits_phi, c, dt, momentum_omegas, t)
        px, py, phi = compute_all_amplitudes(state, qbits_px, qbits_py, qbits_phi, eps, c, N, momentum_omegas)
    return px, py, phi


def experiment_with_potential_time_evolution(qbits_px, qbits_py, qbits_phi, ancillas, px_init, py_init, phi_init, antifermion, c, dt, V0, N, momentum_omegas, eps, t):
    with log_time(__name__, "experiment_with_potential_time_evolution"):
        state = prepare_momentum_eigenstate(len(qbits_px) + len(qbits_py) + len(qbits_phi) + len(ancillas)
                                            , qbits_px, qbits_py, qbits_phi
                                            , px_init, py_init, phi_init, antifermion)
        state = simulate_with_potential(state, qbits_px, qbits_py, qbits_phi, ancillas, c, dt, V0, momentum_omegas, t)
        px, py, phi = compute_all_amplitudes(state, qbits_px, qbits_py, qbits_phi, eps, c, N, momentum_omegas)
    return px, py, phi


def experiment_with_potential_time_evolution_optimized(qbits_px, qbits_py, qbits_phi, ancillas, px_init, py_init, phi_init, antifermion, c, dt, V0, N, momentum_omegas, eps, t):
    with log_time(__name__, "experiment_with_potential_time_evolution"):
        state = prepare_momentum_eigenstate(len(qbits_px) + len(qbits_py) + len(qbits_phi) + len(ancillas)
                                            , qbits_px, qbits_py, qbits_phi
                                            , px_init, py_init, phi_init, antifermion)
        state = simulate_with_potential_optimized(state, qbits_px, qbits_py, qbits_phi, ancillas, c, dt, V0, momentum_omegas, t)
        px, py, phi = compute_all_amplitudes(state, qbits_px, qbits_py, qbits_phi, eps, c, N, momentum_omegas)
    return px, py, phi


def experiment_optimized_scattering_angle(qbits_px, qbits_py, qbits_phi, ancillas, ptot, phi_init, antifermion, c, dt, V0, N, momentum_omegas, eps, angle, t):
    px_init = int(ptot * np.cos(angle))
    py_init = int(ptot * np.sin(angle))
    with log_time(__name__, "experiment_with_potential_scattering_angle"):
        state = prepare_momentum_eigenstate(len(qbits_px) + len(qbits_py) + len(qbits_phi) + len(ancillas)
                                            , qbits_px, qbits_py, qbits_phi
                                            , px_init, 0, phi_init, antifermion)
        state = simulate_with_potential_optimized(state, qbits_px, qbits_py, qbits_phi, ancillas, c, dt, V0, momentum_omegas, t)
        px, py, phi = compute_all_amplitudes(state, qbits_px, qbits_py, qbits_phi, eps, c, N, momentum_omegas)
    return px_init, py_init, px, py, phi
