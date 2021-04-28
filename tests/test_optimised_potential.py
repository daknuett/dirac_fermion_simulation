from itertools import product
import numpy as np

from pyqcs import X, H, list_to_circuit, PrettyState as State

from lib.circuits import CR
from lib.controlled_gate import ncontrolled

input_states = list(product(*([[0,1]] * 8)))
qbits_px = list(range(8))
ancillas = list(range(8, 8 + 5))

print(input_states)


circuit = (list_to_circuit([X(i) for i in qbits_px[-6:]])
            | ncontrolled(qbits_px[0], CR, ancillas, qbits_px[-6:], np.pi / 2)
            | list_to_circuit([X(i) for i in qbits_px[-6:]]))
circuit = ncontrolled(qbits_px[0], CR, ancillas, qbits_px[-6:], np.pi / 2)

print(qbits_px)
print(qbits_px[-6:])


#for config in input_states:
#    print("-"*80)
#    setup_circuit = list_to_circuit([X(i) for i,j in enumerate(config) if j])
#    state = State.new_zero_state(len(ancillas) + len(qbits_px))
#    state = setup_circuit * state
#
#    resulting_state = circuit * state
#
#    print(state)
#    print("->")
#    print(resulting_state)

state = list_to_circuit([H(i) for i in qbits_px]) * State.new_zero_state(len(ancillas) + len(qbits_px))
print(state)
print("->")
print(circuit * state)
