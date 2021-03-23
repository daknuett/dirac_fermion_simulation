import logging
import ray
import json
import numpy as np
from pyqcs.experiment.workflow import WorkflowSpawner

from lib.experiment import experiment_with_potential_scattering_angle
from lib.log_time import log_time

if __name__ == "__main__":
    with log_time(__name__, "setup"):
        c = 1
        dt = 0.01
        eps = 1e-10
        N = 6
        V0 = .5
        antifermion = False

        qbits_phi = [0]
        qbits_px = list(range(1, N + 1))
        qbits_py = list(range(N + 1, 2*N + 1))
        ancilla_qbits = [2*N + 1, 2*N + 2, 2*N + 3, 2*N + 4]

        momentum_omegas = [2**i for i in range(N)]
        momentum_omegas[-1] *= -1

        ptot = 15
        angles = np.arange(0, np.pi / 2, 0.2)
        t = .5

        phi_init = 0.12

        config = {
            "c": c
            , "dt": dt
            , "eps": eps
            , "N": N
            , "V0": V0
            , "antifermion": antifermion
            , "qbits_phi": qbits_phi
            , "qbits_px": qbits_px
            , "qbits_py": qbits_py
            , "ancillas": ancilla_qbits
            , "momentum_omegas": momentum_omegas
            , "ptot": ptot
            , "t": t
            , "phi_init": phi_init
        }

        logging.basicConfig(level=logging.INFO)

        simul2 = lambda a: experiment_with_potential_scattering_angle(
            qbits_px, qbits_py, qbits_phi, ancilla_qbits
            , ptot, phi_init
            , antifermion, c, dt, V0, N
            , momentum_omegas, eps, a, t)

    with log_time(__name__, "set up ray"):
        nworkers = 4
        ray.init()
        spawner = WorkflowSpawner("simulate", [simul2])

        actors = [spawner.spawn() for _ in range(nworkers)]
        pool = ray.util.ActorPool(actors)

    with log_time(__name__, "compute results"):
        results = list(pool.map(lambda a, v: a.execute.remote(v), angles))

    with log_time(__name__, "save results"):
        with open("simulation_scattering_angle.json", "w") as fout:
            data = config
            data.update({"angles": list(angles), "results": results})
            json.dump(data, fout)
