from itertools import product
from pyqcs import State, X, list_to_circuit
from lib.circuits import C2X

configurations = list(product([0,1], [0,1], [0,1]))

for config in configurations:
    print("#" * 60)
    print(config)
    setup = list_to_circuit([X(i) for i,s in enumerate(config) if s])
    state = setup * State.new_zero_state(3)
    print(state)
    print(C2X(2, 1, 0) * state)
