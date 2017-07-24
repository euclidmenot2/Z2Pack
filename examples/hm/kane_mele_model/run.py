#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import z2pack
import numpy as np
from numpy import cos, sin, kron, sqrt
import matplotlib.pyplot as plt

logging.getLogger('z2pack').setLevel(logging.WARNING)

# defining pauli matrices
identity = np.identity(2, dtype=complex)
pauli_x = np.array([[0, 1], [1, 0]], dtype=complex)
pauli_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
pauli_z = np.array([[1, 0], [0, -1]], dtype=complex)

def get_kane_mele_hamiltonian(t, lambda_v, lambda_R, lambda_SO):
    def inner(k):
        k = np.array(k) * 2 * np.pi
        kx, ky, kz = k
        x = kx / 2
        y = sqrt(3) * ky / 2
        return (
            t * (1 + 2 * cos(x) * cos(y)) * kron(pauli_x, identity) +
            lambda_v * kron(pauli_z, identity) +
            lambda_R * (1 - cos(x) * cos(y)) * kron(pauli_y, pauli_x) +
            -sqrt(3) * lambda_R * sin(x) * sin(y) * kron(pauli_y, pauli_y) +
            2 * t * cos(x) * sin(y) * kron(pauli_y, identity) +
            lambda_SO * (2 * sin(2 * x) - 4 * sin(x) * cos(y)) * kron(pauli_z, pauli_z) +
            lambda_R * cos(x) * sin(y) * kron(pauli_x, pauli_x) +
            -sqrt(3) * lambda_R * sin(x) * cos(y) * kron(pauli_x, pauli_y)
        )
    return inner

def get_z2(hamiltonian):
    system = z2pack.hm.System(hamiltonian, bands=2)
    res = z2pack.surface.run(system=system, surface=lambda s, t: [s / 2, t, 0])
    return z2pack.invariant.z2(res)

if __name__ == '__main__':
    print('Z2 invariant: {}'.format(get_z2(get_kane_mele_hamiltonian(t=1, lambda_v=0.1, lambda_R=0.05, lambda_SO=0.06))))
