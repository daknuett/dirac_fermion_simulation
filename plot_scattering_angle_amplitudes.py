import sys
import os
import json
import matplotlib.pyplot as plt
import numpy as np

from lib.dct_statistics import unpack_amplitudes


def plot_data(data):
    fig, (axovw, axphi, axpx) = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(10, 22))
    reslt_data = [i[2:] for i in data["results"]]
    input_data = np.array([i[:2] for i in data["results"]])

    spin_orientation, transmission_amplitude, reflected_amplitudes = unpack_amplitudes(reslt_data, input_data)
    reflection_avg = np.average(reflected_amplitudes, axis=1)
    reflection_std = np.std(reflected_amplitudes, axis=1)

    angles = data["angles"]

    h0, = axovw.plot(angles, spin_orientation, color="C0", label=r"$\bar{\phi}$")
    axovwp = axovw.twinx()
    h1, = axovwp.plot(angles, transmission_amplitude, color="C1", label=r"$T(p_x)$")
    axovw.legend(handles=[h0], loc="upper left")
    axovwp.legend(handles=[h1], loc="upper right")
    axovw.set_title("Overview")
    axovw.set_xlabel("Scattering Angle")
    axovw.set_ylabel("average spin orientation [1]")
    axovwp.set_ylabel("transmission probability")

    h0, = axphi.plot(angles, spin_orientation, color="C0", label=r"$\bar{\phi}$")
    axphi.grid()
    axphi.set_title(r"$\phi$")
    axphi.legend(handles=[h0])
    axphi.set_ylabel("average spin orientation [1]")

    axpx2 = axpx.twinx()
    h2, = axpx2.plot(angles, reflection_avg, color="C3", label=r"$\bar{R}(p_x) \pm \sigma$")
    axpx2.fill_between(angles, reflection_avg + reflection_std, reflection_avg - reflection_std, color="C3", alpha=0.5)
    h0, = axpx.plot(angles, transmission_amplitude, color="C1", label=r"$T(p_x)$")
    axpx.grid()
    axpx.set_title("$T(p_x)$")
    axpx.legend(handles=[h0], loc='upper left')
    axpx.set_ylabel("$T(p_x)$")
    axpx2.legend(handles=[h2], loc='upper right')
    axpx2.set_ylabel(r"$\bar{R}(p_x)$")

    fig.tight_layout(pad=3.)


if __name__ == "__main__":
    default_fname = "simulation_scattering_angle.json"

    if(len(sys.argv) == 1):
        print("no file name supplied, using", default_fname)
        fname = default_fname
    else:
        fname = sys.argv[1]

    if(not os.path.exists(fname)):
        print("FATAL:", fname, "does not exist.")
        sys.exit(1)

    with open(fname) as fin:
        results = json.load(fin)

    print(f"read {len(results['angles'])} data points from {fname}")

    def json2dct(js):
        return {float(k): v for k, v in js.items()}

    results["results"] = [
        [pxinit, pyinit, json2dct(px), json2dct(py), json2dct(phi)]
            for pxinit, pyinit, px, py, phi in results["results"]
    ]
    plot_data(results)
    plt.show()
