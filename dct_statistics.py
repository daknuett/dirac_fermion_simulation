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
