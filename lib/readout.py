from pyqcs import compute_amplitudes

from .log_time import log_time


def res2momentum(res, c, N, momentum_omegas):
    result = 0
    for bit in range(N):
        if(res & (1 << bit)):
            result += momentum_omegas[bit]
    result *= c / 2**N
    return result


def shift_integer_result(res, qbits):
    return res >> min(qbits)


def read_all_amplitudes(state, qbits_px, qbits_py, qbits_phi, eps):
    with log_time(__name__, "read_all_amplitudes"):
        px = compute_amplitudes(state, qbits_px, eps)
        if(qbits_py):
            py = compute_amplitudes(state, qbits_py, eps)
        else:
            py = {0: 1}
        phi = compute_amplitudes(state, qbits_phi, eps)
        px = {shift_integer_result(k, qbits_px): v for k,v in px.items()}
        if(qbits_py):
            py = {shift_integer_result(k, qbits_py): v for k,v in py.items()}
        phi = {shift_integer_result(k, qbits_phi): v for k,v in phi.items()}

    return (px, py, phi)


def compute_all_amplitudes(state, qbits_px, qbits_py, qbits_phi, eps, c, N, momentum_omegas):
    px, py, phi = read_all_amplitudes(state, qbits_px, qbits_py, qbits_phi, eps)
    px = {res2momentum(res, c, N, momentum_omegas): v for res,v in px.items()}
    py = {res2momentum(res, c, N, momentum_omegas): v for res,v in py.items()}
    return px, py, phi


def compute_all_amplitudes_no_conversion(state, qbits_px, qbits_py, qbits_phi, eps, c, N, momentum_omegas):
    px, py, phi = read_all_amplitudes(state, qbits_px, qbits_py, qbits_phi, eps)
    return px, py, phi
