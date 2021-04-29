import json
import sys

import numpy as np
import matplotlib.pyplot as plt

from lib.readout import I2F
from lib.dct_statistics import get_expectation_value, get_reflected, get_transmitted, get_std


default_fname = "simulation_with_potential_optimized.json"

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


data["results"] = [[json2idict(px), json2idict(py), json2fdict(phi)]
                    for px, py, phi in data["results"]]

i2f = I2F(data["c"], data["N"], data["momentum_omegas"])

px_init = i2f(data["px_init"])
py_init = i2f(data["py_init"])

negative_inital_px = False
if(px_init < 0):
    negative_inital_px = True
negative_inital_py = False
if(py_init < 0):
    negative_inital_py = True

expectation_values = np.array([[get_expectation_value(px, i2f)
                                , get_expectation_value(py, i2f)
                                , get_expectation_value(phi, lambda x:x)]
                                    for px, py, phi in data["results"]])

stddevs = np.array([[get_std(px, i2f), get_std(py, i2f)]
                        for px, py, phi in data["results"]])

transmitted_expect = np.array([[get_expectation_value(get_transmitted(px, i2f, negative_inital_px), i2f)
                        , get_expectation_value(get_transmitted(py, i2f, negative_inital_py), i2f)]
                            for px, py, phi in data["results"]])
reflected_expect = np.array([[get_expectation_value(get_reflected(px, i2f, negative_inital_px), i2f)
                        , get_expectation_value(get_reflected(py, i2f, negative_inital_py), i2f)]
                            for px, py, phi in data["results"]])
reflected_std = np.array([[get_std(get_reflected(px, i2f, negative_inital_px), i2f)
                        , get_std(get_reflected(py, i2f, negative_inital_py), i2f)]
                            for px, py, phi in data["results"]])

time = data["time"]

fig, (axovw, axpx, axpy) = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(10,15))

h0, = axovw.plot(time, expectation_values[:,2], color="C0", label=r"$\overline{\phi}$")
axovwp = axovw.twinx()
h1, = axovwp.plot(time, expectation_values[:,0], color="C1", label=r"$\overline{p_x}$")
h2, = axovwp.plot(time, expectation_values[:,1], color="C4", label=r"$\overline{p_y}$")
axovw.legend(handles=[h0], loc="upper left")
axovwp.legend(handles=[h1, h2], loc="upper right")
axovw.set_title("Overview")
axovw.set_xlabel("Time [arbitrary units]")
axovw.set_ylabel("average spin orientation [1]")
axovwp.set_ylabel("average momentum")


axpx2 = axpx.twinx()
h1, = axpx.plot(time, transmitted_expect[:,0], color="C2", label=r"$\overline{p_{x,T}}$")
h0, = axpx.plot(time, expectation_values[:,0], color="C1", label=r"$\overline{p_x}$")
#h0, = axpx.plot(time, expectation_values[:,0], color="C1", label=r"$\overline{p_x} \pm \sigma$")
#axpx.fill_between(time, expectation_values[:,0] + stddevs[:,0], expectation_values[:,0] - stddevs[:,0], color="C1", alpha=0.5)

h2, = axpx2.plot(time, reflected_expect[:,0], color="C3", label=r"$\overline{p_{x,R}}$")
#axpx2.fill_between(time, reflected_expect[:,0] + reflected_std[:,0], reflected_expect[:,0] - reflected_std[:,0], color="C3", alpha=0.5)
axpx.grid()
axpx.set_title("$p_x$")
axpx.legend(handles=[h0, h1], loc='upper left')
axpx.set_ylabel("$p_x$")
axpx2.legend(handles=[h2], loc='upper right')
axpx2.set_ylabel("Reflected $p_x$")


axpy2 = axpy.twinx()
h1, = axpy.plot(time, transmitted_expect[:,1], color="C5", label=r"$\overline{p_{y,T}}$")
h0, = axpy.plot(time, expectation_values[:,1], color="C4", label=r"$\overline{p_y}$")
#h0, = axpy.plot(time, expectation_values[:,1], color="C4", label=r"$\overline{p_y} \pm \sigma$")
#axpy.fill_between(time, expectation_values[:,1] + stddevs[:,1], expectation_values[:,1] - stddevs[:,1], color="C4", alpha=0.5)

h2, = axpy2.plot(time, reflected_expect[:,1], color="C6", label=r"$\overline{p_{y,R}}$")
#axpy2.fill_between(time, reflected_expect[:,1] + reflected_std[:,1], reflected_expect[:,1] - reflected_std[:,1], color="C6", alpha=0.5)
axpy.grid()
axpy.set_title("$p_y$")
axpy.legend(handles=[h0, h1], loc='upper left')
axpy.set_ylabel("$p_y$")
axpy2.legend(handles=[h2], loc='upper right')
axpy2.set_ylabel("Reflected $p_y$")

plt.show()
