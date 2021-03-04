from pyqcs import (X, H, S, R, CX
                   , list_to_circuit)

def CRX(act, control, phi):
    return (CX(act, control) 
            | (H(act) | R(act, -phi) | X(act) | R(act, phi) | X(act) | H(act))
            | CX(act, control))


def CRY(act, control, phi):
    return (CX(act, control) 
            | (S(act) | H(act) | R(act, -phi) | X(act) | R(act, phi) | X(act) | H(act) | S(act).get_dagger())
            | CX(act, control))


def RZ(act, phi):
    return R(act, -phi) | X(act) | R(act, phi) | X(act)


def T(act):
    return R(act, np.pi / 8)
def C2X(act, c1, c2):
    return (
        H(act) | CX(act, c2) | T(act).get_dagger() | CX(act, c1)
        | T(act) | CX(act, c2) | T(act).get_dagger() | CX(act, c1)
        | T(act) | H(act) | T(c2).get_dagger() | CX(c2, c1)
        | T(c2).get_dagger() | CX(c2, c1) | T(c1) | S(c2)
    )

def CR(act, control, phi):
    return (R(act, phi/2) | CX(act, control)
            | R(act, -phi/2) | R(control, phi/2) 
            | CX(act, control)
           )
    
def control5_handthrough(controls, ancillas):
    circuit = [C2X(ancillas[0], controls[0], controls[1])]
    for i, cancilla in enumerate(ancillas[:-1]):
        circuit.append(C2X(ancillas[i+1], controls[i+2], cancilla))
    return list_to_circuit(circuit)

def C5X(act, controls, ancillas):
    return (control5_handthrough(controls, ancillas)
            | CX(act, ancillas[-1])
            | control5_handthrough(controls, ancillas).get_dagger()
           )
def C5R(act, controls, ancillas, phi):
    return (control5_handthrough(controls, ancillas)
            | CR(act, ancillas[-1], phi)
            | control5_handthrough(controls, ancillas).get_dagger()
           )
