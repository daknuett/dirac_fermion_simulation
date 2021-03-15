import logging
import ray
import json
import numpy as np
from pyqcs.experiment.workflow import WorkflowSpawner

from lib.experiment import experiment_free_case_time_evolution
from lib.log_time import log_time

if __name__ == "__main__":
    with log_time(__name__, "setup"):
        c = 1
        dt = 0.001
        eps = 1e-10
        N = 8
        antifermion = False

        qbits_phi = [0]
        qbits_px = list(range(1, 9))
        qbits_py = list(range(9, 17))
        ancilla_qbits = [17, 18, 19, 20]

        momentum_omegas = [2**i for i in range(N)]
        momentum_omegas[-1] *= -1

        px_init = 15
        py_init = 70
        phi_init = 0.12

        logging.basicConfig(level=logging.INFO)

        simul2 = lambda t: experiment_free_case_time_evolution(qbits_px, qbits_py, qbits_phi, px_init, py_init, phi_init, antifermion, c, dt, N, momentum_omegas, eps, t)
        time = np.arange(0.1, .4, 0.007)

    with log_time(__name__, "set up ray"):
        nworkers = 4
        ray.init()
        spawner = WorkflowSpawner("simulate", [simul2])

        actors = [spawner.spawn() for _ in range(nworkers)]
        pool = ray.util.ActorPool(actors)

    with log_time(__name__, "compute results"):
        results = list(pool.map(lambda a,v: a.execute.remote(v), time))

    with log_time(__name__, "save results"):
        with open("simulation_free_case_large_py_small_window.json", "w") as fout:
            json.dump({"time": list(time), "results": results}, fout)
