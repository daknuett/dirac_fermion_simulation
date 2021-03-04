import sys
import os
import json
import matplotlib.pyplot as plt
import numpy as np

from dct_statistics import avg, stddev

default_fname = "simulation_free_case.json"

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

print(f"read {len(results['time'])} data points from {fname}")

def json2dct(js):
    return {float(k):v for k,v in js.items()}

results["results"] = [[json2dct(px), json2dct(py), json2dct(phi)] for px, py, phi in results["results"]]

def plot_data(data):
    fig, (axovw, axphi, axpx, axpy) = plt.subplots(nrows=4, ncols=1, sharex=True, figsize=(18, 10))
    avgs = np.array([[avg(px), avg(py), avg(phi)] for px, py, phi in data["results"]])
    stddevs = np.array([[stddev(px), stddev(py), stddev(phi)] for px, py, phi in data["results"]])
    time = data["time"]

    h0, = axovw.plot(time, avgs[:,2], "r", label=r"$\bar{\phi}$")
    axovwp = axovw.twinx()
    h1, = axovwp.plot(time, avgs[:,0], "g", label=r"$\bar{p_x}$")
    h2, = axovwp.plot(time, avgs[:,1], "b", label=r"$\bar{p_y}$")
    axovw.legend(handles=[h0])
    axovwp.legend(handles=[h1, h2], loc=1)
    axovw.set_title("Overview")
    axovw.set_xlabel("Time [arbitrary units]")
    axovw.set_ylabel("average spin orientation [1]")
    axovwp.set_ylabel("average momentum")

    axphi.plot(time, avgs[:,2], "r", label=r"$\bar{\phi}$")
    axphi.set_title("$\phi$")

    axpx.plot(time, avgs[:,0], "g", label=r"$\bar{p_x} \pm \sigma$")
    axpx.fill_between(time, avgs[:,0] + stddevs[:,0], avgs[:,0] - stddevs[:,0], color="g", alpha=0.5)
    axpx.set_title("$p_x$")

    axpy.plot(time, avgs[:,1], "b", label=r"$\bar{p_y} \pm \sigma$")
    axpy.fill_between(time, avgs[:,1] + stddevs[:,1], avgs[:,1] - stddevs[:,1], color="b", alpha=0.5)
    axpy.set_title("$p_y$")

plot_data(results)
