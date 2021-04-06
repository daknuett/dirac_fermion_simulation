from itertools import product
import numpy as np
import timeit
import logging

from lib.state_preparation import prepare_momentum_eigenstate
from lib.readout import read_all_amplitudes


def test_prepare_momentum_eigenstate_immideate_momentum_readout(ptest):
    nqbits = 17
    qbits_phi = [0]
    qbits_px = list(range(1, 9))
    qbits_py = list(range(9, 17))
    eps = 1e-8

    for px, py in product(ptest, ptest):
        state = prepare_momentum_eigenstate(nqbits, qbits_px, qbits_py, qbits_phi, px, py, 0, False)
        pxread, pyread, phiread = read_all_amplitudes(state, qbits_px, qbits_py, qbits_phi, eps)

        assert len(pxread) == 1
        assert len(pyread) == 1

        assert px in pxread
        if(py not in pyread):
            print(py, pyread)
        assert py in pyread

        assert np.allclose(pxread[px], 1)
        assert np.allclose(pyread[py], 1)


if __name__ == "__main__":
    ptest = [1, 2, 4, 15, 123, 231, 255, 0]
    npretest = 1
    logging.basicConfig(level=logging.INFO)

    rslt = timeit.timeit(lambda:test_prepare_momentum_eigenstate_immideate_momentum_readout([1]), number=npretest) / npretest
    print(f"Test on 1x1 matrix took {rslt}s.")
    print(f"Test matrix is {len(ptest)}x{len(ptest)}.")
    print(f"Entire test is expected to take {rslt*len(ptest)**2}s")

    test_prepare_momentum_eigenstate_immideate_momentum_readout(ptest)
