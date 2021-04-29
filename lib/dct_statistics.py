def modus(values):
    return max(values.items(), key=lambda x: x[1])


def get_transmitted(values, i2f, negative_input=False):
    if not negative_input:
        return {k:v for k,v in values.items() if i2f(k) > 0}
    else:
        return {k:v for k,v in values.items() if i2f(k) < 0}


def get_reflected(values, i2f, negative_input=False):
    if not negative_input:
        return {k:v for k,v in values.items() if i2f(k) < 0}
    else:
        return {k:v for k,v in values.items() if i2f(k) > 0}


def get_expectation_value(values, i2f, f=lambda x:x):
    return sum(f(i2f(k))*v for k,v in values.items())


def get_std(values, i2f):
    return (get_expectation_value(values, i2f, lambda x:x**2)
                - get_expectation_value(values, i2f)**2)**.5
