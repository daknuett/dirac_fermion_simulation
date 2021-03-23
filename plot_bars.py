import sys
import os
import json
import matplotlib.pyplot as plt
import numpy as np


def plot_data(data):
    time = data["time"]
    nplots = len(time)

    ncols = int(np.sqrt(nplots))
    if(ncols**2 == nplots):
        nrows = ncols
    else:
        nrows = ncols + 1

    fig, subplots = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols*4, nrows*4))
    subplots = subplots.reshape(nrows*ncols)

    for i,(dentry, ax) in enumerate(zip(data["results"], subplots)):
        xy = np.array([[k,v] for k,v in sorted(dentry[0].items(), key=lambda x:x[1])[:-1]])
        y = np.log(xy[:,1] + 1)
        #y = xy[:,1]
        ax.bar(xy[:,0], y, width=1e-2)

        ax.set_title(f"$t = {time[i]:.3e}$")
        ax.set_xlabel("$p_x$ without modus")
        ax.set_ylabel(r"$\log(P + 1)$")
        #ax.set_ylabel(r"$P$")

    fig.tight_layout(pad=4.)


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
