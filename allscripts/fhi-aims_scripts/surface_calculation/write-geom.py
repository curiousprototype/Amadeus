#!/usr/bin/python

import sys
from math import sqrt

def output_lattice_vector(x, y, z):
    print("lattice_vector  %.16f  %.16f  %.16f" % (x, y, z))
def output_atom(x, y, z, name):
    print("atom %.16f  %.16f  %.16f  %s" % (x, y, z, name))
def output_constrained_atom(x, y, z, name):
    print("atom %.16f  %.16f  %.16f  %s" % (x, y, z, name))
    print("  constrain_relaxation .true.")

A = 5.416            # Lattice constant
L_vac = 30.          # Vacuum
A_1x1 = A/sqrt(2.)   # 1x1 surface periodicity
n_layer = 4          # Number of layers in z-direction
Z = A/4.             # Layer separation in z-direction
C = 0.5 * A_1x1      # Row separation in x- and y-direction

# H-saturation is put at this fraction of where the next
# Si atom would have been.
frac_H = 0.63

# (2x1) reconstructed lattice:
output_lattice_vector(2*A_1x1, 0.,    0.)
output_lattice_vector(0.,      A_1x1, 0.)
output_lattice_vector(0.,      0.,    n_layer*Z+L_vac)
print

# Hydrogen saturation
# The next Si would have been at (+/-C, 0., -Z).
output_atom(   -frac_H*C, 0., -frac_H*Z, "H")
output_atom(   +frac_H*C, 0., -frac_H*Z, "H")
# The next Si would have been at (2*C+/-C, 0., -Z).
output_atom(2*C-frac_H*C, 0., -frac_H*Z, "H")
output_atom(2*C+frac_H*C, 0., -frac_H*Z, "H")
# Bottom Si layer
output_atom(0*C, 0., 0*Z, "Si")
output_atom(2*C, 0., 0*Z, "Si")
# Other Si layers
output_atom(0*C, C,  1*Z, "Si")
output_atom(2*C, C,  1*Z, "Si")
output_atom(1*C, C,  2*Z, "Si")
output_atom(3*C, C,  2*Z, "Si")
output_atom(1*C, 0., 3*Z, "Si")
output_atom(3*C, 0., 3*Z, "Si")
