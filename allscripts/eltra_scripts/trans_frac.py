import numpy as np
from ase.io import read, write

geo_file = input('geometry.in in real coordinate: ')
out_file = input('output frac geometry filename: ')

real_coord = read(geo_file, format='aims')
print(real_coord.positions)
write( out_file, real_coord,scaled=True, format='aims')

