import json
import sys

import numpy as np
import matplotlib.pyplot as plt

from lib.readout import I2F
from lib.dct_statistics import (get_expectation_value
                                , get_reflected
                                , get_transmitted
                                , get_std
                                , get_amplitude)


default_fname = "simulation_scattering_angle.json"

if(len(sys.argv) < 2):
    print("no filename supplied, using", default_fname)
    fname = default_fname
else:
    fname = sys.argv[1]

with open(fname, "r") as fin:
    data = json.load(fin)


def json2fdict(js):
    return {float(k): v for k, v in js.items()}


def json2idict(js):
    return {int(k): v for k, v in js.items()}


data["results"] = [[px_init, py_init, json2idict(px), json2idict(py), json2fdict(phi)]
                    for px_init, py_init, px, py, phi in data["results"]]

i2f = I2F(data["c"], data["N"], data["momentum_omegas"])

angles = data["angles"]

# XXX: Here we assume we only have incoming amplitudes
# with positive momentum.
negative_inital_px = False
negative_inital_py = False

expectation_values = np.array([[get_expectation_value(px, i2f)
                                , get_expectation_value(py, i2f)
                                , get_expectation_value(phi, lambda x:x)]
                                    for px_init, py_init, px, py, phi in data["results"]])

stddevs = np.array([[get_std(px, i2f), get_std(py, i2f)]
                        for px_init, py_init, px, py, phi in data["results"]])

transmitted_expect = np.array([[get_expectation_value(get_transmitted(px, i2f, negative_inital_px), i2f)
                        , get_expectation_value(get_transmitted(py, i2f, negative_inital_py), i2f)]
                            for px_init, py_init, px, py, phi in data["results"]])
reflected_expect = np.array([[get_expectation_value(get_reflected(px, i2f, negative_inital_px), i2f)
                        , get_expectation_value(get_reflected(py, i2f, negative_inital_py), i2f)]
                            for px_init, py_init, px, py, phi in data["results"]])
reflected_std = np.array([[get_std(get_reflected(px, i2f, negative_inital_px), i2f)
                        , get_std(get_reflected(py, i2f, negative_inital_py), i2f)]
                            for px_init, py_init, px, py, phi in data["results"]])
incident_p = np.array([[px_init, py_init]
                            for px_init, py_init, px, py, phi in data["results"]])
transmitted_amplitude = np.array([get_amplitude(get_transmitted(px, i2f, negative_inital_px))
                            for px_init, py_init, px, py, phi in data["results"]])
reflected_amplitude = np.array([get_amplitude(get_reflected(px, i2f, negative_inital_px))
                            for px_init, py_init, px, py, phi in data["results"]])


fig, (ax_momenta, ax_relmomenta, ax_amplitudes) = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(10, 15))

ax_momenta.set_title("Momentum Expectation Values")
h0, = ax_momenta.plot(angles, expectation_values[:,0], "C1", label=r"$\overline{p_x}$")
ax_momenta2 = ax_momenta.twinx()
h1, = ax_momenta.plot(angles, transmitted_expect[:,0], "C2", label=r"$\overline{p_{x,T}}$")
h2, = ax_momenta2.plot(angles, reflected_expect[:,0], "C3", label=r"$\overline{p_{x,R}}$")
ax_momenta.set_ylabel(r"Momentum $\overline{p_x}, \overline{p_{x,T}}$")
ax_momenta2.set_ylabel(r"Reflected Momentum $\overline{p_{x,R}}$")
ax_momenta.set_xlabel(r"Incident Angle $\phi$")
ax_momenta.legend(handles=[h0, h1, h2])

ax_relmomenta.set_title("Expectation Values Normalized to Incident Momentum")
h0, = ax_relmomenta.plot(angles, transmitted_expect[:,0] / incident_p[:,0], "C2", label=r"$\frac{\overline{p_{x,T}}}{p_{x,I}}$")
ax_relmomenta2 = ax_relmomenta.twinx()
h1, = ax_relmomenta2.plot(angles, reflected_expect[:,0] / incident_p[:,0], "C3", label=r"$\frac{\overline{p_{x,R}}}{p_{x,I}}$")
ax_relmomenta.set_ylabel(r"Normalized Transmitted Momentum")
ax_relmomenta2.set_ylabel(r"Normalized Reflected Momentum")
ax_momenta.set_xlabel(r"Incident Angle $\phi$")
ax_relmomenta.legend(handles=[h0, h1])

ax_amplitudes.set_title("Amplitudes")
h0, = ax_amplitudes.plot(angles, transmitted_amplitude, "C2", label=r"Transmitted Amplitude")
ax_amplitudes2 = ax_amplitudes.twinx()
h1, = ax_amplitudes2.plot(angles, reflected_amplitude, "C3", label=r"Reflected Amplitude")
ax_amplitudes.set_ylabel(r"Transmitted Amplitude")
ax_amplitudes2.set_ylabel(r"Reflected Amplitude")
ax_amplitudes.set_xlabel(r"Incident Angle $\phi$")
ax_amplitudes.legend(handles=[h0, h1])

plt.show()
