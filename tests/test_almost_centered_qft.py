import numpy as np
from pyqcs import X, PrettyState as State
#from lib.qft import QFT
from lib.qft import QFT

import matplotlib.pyplot as plt

nqbits = 7

state = State.new_zero_state(nqbits)


def i2si_(x):
    shift = nqbits - 1
    if(not (x & (1 << shift))):
        return x
    x ^= (1 << shift)
    x -= (1 << shift)
    return x


i2si = np.vectorize(i2si_)


def qft(X):
    Y = np.zeros_like(X)
    N = len(X)
    for j,_ in enumerate(Y):
        for i,xi in enumerate(X):
            Y[j] += xi * np.exp(2*np.pi*1j * i2si(j) * i2si(i) / N)
    Y /= np.sqrt(N)
    return Y


result = QFT(list(range(nqbits))) * state
transformed = qft(state._qm_state)
assert np.allclose(result._qm_state, transformed)
#print("QFT of |0>:")
#print(result)

state = X(0) * State.new_zero_state(nqbits)  # |1>
result = QFT(list(range(nqbits))) * state
transformed = qft(state._qm_state)
print("expected:")
print(transformed)
print("got:")
print(result._qm_state)
fig, (re, im) = plt.subplots(nrows=2, ncols=1, sharex=True)
T = [i2si(i) for i,_ in enumerate(result._qm_state)]
h0, = re.plot(T, result._qm_state.real, ".", label="got")
h1, = re.plot(T, transformed.real, ".", label="expect")
re.legend(handles=[h0, h1])
re.set_title("real")
re.grid()
h0, = im.plot(T, result._qm_state.imag, ".", label="got")
h1, = im.plot(T, transformed.imag, ".", label="expect")
im.legend(handles=[h0, h1])
im.set_title("imag")
im.grid()
plt.show()

#assert np.allclose(result._qm_state, transformed)
#print("QFT of |1>:")
#print(result)

state = X(1) * State.new_zero_state(nqbits)  # |2>
result = QFT(list(range(nqbits))) * state
transformed = qft(state._qm_state)
assert np.allclose(result._qm_state, transformed)
#print("QFT of |2>:")
#print(result)
fig, (re, im) = plt.subplots(nrows=2, ncols=1, sharex=True)
T = [i2si(i) for i,_ in enumerate(result._qm_state)]
h0, = re.plot(T, result._qm_state.real, ".", label="got")
h1, = re.plot(T, transformed.real, ".", label="expect")
re.legend(handles=[h0, h1])
re.set_title("real")
re.grid()
h0, = im.plot(T, result._qm_state.imag, ".", label="got")
h1, = im.plot(T, transformed.imag, ".", label="expect")
im.legend(handles=[h0, h1])
im.set_title("imag")
im.grid()
plt.show()
