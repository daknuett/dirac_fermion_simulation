import warnings
from pyqcs import list_to_circuit
from .circuits import C2X


def ncontrolled(act, cgate, ancillas, controls, *args):
    """
    Takes an 1-controlled gate ``cgate`` and builds an ``n``-controlled
    gate, where ``n = len(controls)`` using the ``n - 1`` ``ancillas``.
    ``*args`` will be passed to ``cgate`` after the act and control arguments.
    """
    if(len(ancillas) < len(controls) - 1):
        raise ValueError(f"need len(controls) - 1 ancillas (expected {len(controls)  -1}, got {len(ancillas)})")
    if(len(ancillas) > len(controls) - 1):
        warnings.warn(f"excessive ancilla qbits used, this may lead to bad performance (expected {len(controls)  -1}, got {len(ancillas)})", ResourceWarning)
    ancillas = ancillas[:len(controls) - 1]

    handthrough_circuit = [C2X(ancillas[0], controls[0], controls[1])]
    for i, cancilla in enumerate(ancillas[:-1]):
        handthrough_circuit.append(C2X(ancillas[i + 1], controls[i + 2], cancilla))
    handthrough_circuit = list_to_circuit(handthrough_circuit)

    return handthrough_circuit | cgate(act, ancillas[-1], *args) | handthrough_circuit.get_dagger()
