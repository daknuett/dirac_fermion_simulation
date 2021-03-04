
def avg(vls):
    return sum(k * v for k,v in vls.items())

def sqravg(vls):
    return sum(k**2 * v for k,v in vls.items())

def stddev(vls):
    return abs(sqravg(vls) - avg(vls)**2)**0.5
