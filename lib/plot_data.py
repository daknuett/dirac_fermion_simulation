import sys
import os
import json
import matplotlib.pyplot as plt
import numpy as np

from dct_statistics import avg, stddev, modus, avg_allbutmodus, stddev_allbutmodus


def plot_data(data):
    fig, (axovw, axphi, axpx, axpy) = plt.subplots(nrows=4, ncols=1, sharex=True, figsize=(10, 22))
    avgs = np.array([[avg(px), avg(py), avg(phi)] for px, py, phi in data["results"]])
    stddevs = np.array([[stddev(px), stddev(py), stddev(phi)] for px, py, phi in data["results"]])
    modi = np.array([[modus(px), modus(py), modus(phi)] for px, py, phi in data["results"]])
    avg_butmodi = np.array([[avg_allbutmodus(px), avg_allbutmodus(py), avg_allbutmodus(phi)] for px, py, phi in data["results"]])
    stddev_modi = np.array([[stddev_allbutmodus(px), stddev_allbutmodus(py), stddev_allbutmodus(phi)] for px, py, phi in data["results"]])
    time = data["time"]

    h0, = axovw.plot(time, avgs[:,2], color="C0", label=r"$\bar{\phi}$")
    axovwp = axovw.twinx()
    h1, = axovwp.plot(time, avgs[:,0], color="C1", label=r"$\bar{p_x}$")
    h2, = axovwp.plot(time, avgs[:,1], color="C2", label=r"$\bar{p_y}$")
    axovw.legend(handles=[h0], loc="upper left")
    axovwp.legend(handles=[h1, h2], loc="upper right")
    axovw.set_title("Overview")
    axovw.set_xlabel("Time [arbitrary units]")
    axovw.set_ylabel("average spin orientation [1]")
    axovwp.set_ylabel("average momentum")

    h0, = axphi.plot(time, avgs[:,2], color="C0", label=r"$\bar{\phi}$")
    axphi.grid()
    axphi.set_title(r"$\phi$")
    axphi.legend(handles=[h0])
    axphi.set_ylabel("average spin orientation [1]")

    axpx2 = axpx.twinx()
    h2, = axpx2.plot(time, avg_butmodi[:,0], color="C3", label=r"With modus removed")
    axpx2.fill_between(time, avg_butmodi[:,0] + stddev_modi[:,0], avg_butmodi[:,0] - stddev_modi[:,0], color="C3")
    h0, = axpx.plot(time, avgs[:,0], color="C1", label=r"$\bar{p_x} \pm \sigma$")
    axpx.fill_between(time, avgs[:,0] + stddevs[:,0], avgs[:,0] - stddevs[:,0], color="C1", alpha=0.5)
    h1, = axpx.plot(time, modi[:,0], ".", color="C1", label=r"modus$(p_x)$")
    axpx.grid()
    axpx.set_title("$p_x$")
    axpx.legend(handles=[h0, h1], loc='upper left')
    axpx.set_ylabel("$p_x$")
    axpx2.legend(handles=[h2], loc='upper right')
    axpx2.set_ylabel("$p_x - m(p_x)$")

    axpy2 = axpy.twinx()
    h2, = axpy2.plot(time, avg_butmodi[:,1], color="C4", label=r"With modus removed")
    axpy2.fill_between(time, avg_butmodi[:,1] + stddev_modi[:,1], avg_butmodi[:,1] - stddev_modi[:,1], color="C4")
    h0, = axpy.plot(time, avgs[:,1], color="C2", label=r"$\bar{p_y} \pm \sigma$")
    axpy.fill_between(time, avgs[:,1] + stddevs[:,1], avgs[:,1] - stddevs[:,1], color="C2", alpha=0.5)
    h1, = axpy.plot(time, modi[:,1], ".", color="C2", label=r"modus$(p_y)$")
    axpy.grid()
    axpy.set_title("$p_y$")
    axpy.legend(handles=[h0, h1], loc='upper left')
    axpy.set_ylabel("$p_y$")
    axpy2.legend(handles=[h2], loc='upper right')
    axpy2.set_ylabel("$p_y - m(p_y)$")

    fig.tight_layout(pad=3.)


if __name__ == "__main__":
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
        return {float(k): v for k, v in js.items()}

    results["results"] = [
        [json2dct(px), json2dct(py), json2dct(phi)]
            for px, py, phi in results["results"]
    ]
    plot_data(results)
    plt.show()
