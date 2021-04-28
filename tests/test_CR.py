import numpy as np
from pyqcs import H, list_to_circuit, PrettyState as State
from lib.circuits import CRI

state = list_to_circuit([H(i) for i in range(2)]) * State.new_zero_state(2)

print(state)
print("->")
print(CRI(0, 1, np.pi / 2) * state)
