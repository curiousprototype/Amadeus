#!/usr/bin/python
import os
import numpy as np

# Minimal lattice constant in A (from run script)
aMin = 5.1
# Maximal lattice constant in A (from run script)
aMax = 5.7
# Sampling density in A (from run script)
step = 0.1
#Number of basis atoms
atom_no = 2

# Number of calculations
n = int(np.rint((aMax - aMin)/step)) + 1

data = open("energies.dat",'w')
data.write("#%22s   %20s\n" % ("lattice constant (AA)","energy (eV/atom)"))

for i in range(n):
   aLat = round((aMin + step * i),1)
   print("Postprocessing lattice constant %10.6f AA." % aLat)
   dirname = str(aLat)
   filename = dirname + "/" + "aims.out"
   # Check if calculation was running
   if (not os.path.isfile(filename)):
      print("%s was not processed." % filename)
   else:
      # Check for convergence
      f = open(filename,'r')
      converged = False
      for line in f:
         if "Have a nice day" in line:
            converged = True
         if "Self-consistency cycle converged." in line:
            converged = True
      f.close()

      if (not converged):
         print("%s is not converged." % filename)
      else:
         # Grep for total energy
         f = open(filename,'r')
         for line in f:
            if "Total energy corr" in line:
               linesplit = line.split()
               energy = float(linesplit[5])/float(atom_no)
               data.write(" %16.6f   %23.6f\n" % (aLat,energy))
         f.close()
data.close()
