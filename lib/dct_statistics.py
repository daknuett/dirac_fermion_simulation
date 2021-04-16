import numpy as np


def avg(vls):
    return sum(k * v for k,v in vls.items())


def sqravg(vls):
    return sum(k**2 * v for k,v in vls.items())


def stddev(vls):
    return abs(sqravg(vls) - avg(vls)**2)**0.5


def modus(vls):
    return max(vls.items(), key=lambda x: x[1])[0]


def avg_allbutmodus(vls):
    return sum(k * v for k,v in sorted(vls.items(), key=lambda x: x[1])[1:])


def sqravg_allbutmodus(vls):
    return sum(k**2 * v for k,v in sorted(vls.items(), key=lambda x: x[1])[1:])


def stddev_allbutmodus(vls):
    return abs(sqravg_allbutmodus(vls) - avg_allbutmodus(vls)**2)**2


def remove_input_amplitude(dct, ipt):
    dct = dict(dct)  # copy
    del(dct[ipt])
    return dct


def get_reflected_amplitudes(dct, ipt):
    refl = remove_input_amplitude(dct, ipt)
    return list(refl.values())


def unpack_amplitudes(reslt_data, input_data):
    transmission_amplitude = np.array([reslt_data[i][0][input_data[i, 0]] for i,_ in enumerate(reslt_data)])
    spin_orientation = np.array([d[2][1] for d in reslt_data])
    reflected_amplitudes = np.array([get_reflected_amplitudes(d[0], input_data[i, 0]) for i,d in enumerate(reslt_data)])

    return spin_orientation, transmission_amplitude, reflected_amplitudes
