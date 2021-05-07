import logging
import ray
import json
import numpy as np
from pyqcs.experiment.workflow import WorkflowSpawner

from lib.experiment import experiment_optimized_scattering_angle
from lib.log_time import log_time

if __name__ == "__main__":
    with log_time(__name__, "setup"):
        c = 1
        dt = 0.005
        eps = 1e-10
        N = 8
        V0 = 144.5
        antifermion = False

        qbits_phi = [0]
        qbits_px = list(range(1, N + 1))
        qbits_py = []
        ancilla_qbits = list(range(N + 1, N + 1 + 5))

        momentum_omegas = [2**i for i in range(N)]
        momentum_omegas[-1] *= -1

        P = np.arange(1, 90, 2, dtype=int)
        t = 7.5

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
            , "t": t
            , "phi_init": phi_init
        }

        logging.basicConfig(level=logging.INFO)

        simul2 = lambda p: experiment_optimized_scattering_angle(
            qbits_px, qbits_py, qbits_phi, ancilla_qbits
            , p, phi_init
            , antifermion, c, dt, V0, N
            , momentum_omegas, eps, t)

    with log_time(__name__, "set up ray"):
        nworkers = 4
        ray.init()
        spawner = WorkflowSpawner("simulate", [simul2])

        actors = [spawner.spawn() for _ in range(nworkers)]
        pool = ray.util.ActorPool(actors)

    with log_time(__name__, "compute results"):
        results = list(pool.map(lambda a, v: a.execute.remote(v), P))

    with log_time(__name__, "save results"):
        with open("simulation_px_sweep.json", "w") as fout:
            data = config
            data.update({"angles": list(P), "results": results})
            json.dump(data, fout)
