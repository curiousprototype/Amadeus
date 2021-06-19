###########################################################################################################################################################################################
# This is a simple example how to analyze the results from the distance series                                                                                                            #
###########################################################################################################################################################################################

from numpy import *
from sys import argv
filename=argv[1]
i_step = 0                                                                    # number of relax. steps
max_force = []                                                                # empty list for max force component
Energy = []                                                                   # empty list for energy
N = None                                                                      # Number of atoms
at = None                                                                     # atoms counter
atoms=[]                                                                      # atoms list
for line in open(filename):                                                   # Loop through file and extract energy
    if 'Number of atoms' in line:
      N=(int(line.split()[-1]))                                               # Set Number of atoms
    if 'Maximum force component' in line:
      max_force.append(float(line.split()[-2]))                               # Get force and enumerate relax. step
      i_step += 1                                                             
    if 'Total energy uncorrected' in line:
      Energy.append(float(line.split()[-2]))                                  # Get energy
    if '| Atomic structure' in line:
      at=0                                                                    # Set atom counter, initital geometry
    if 'Updated atomic structure:' in line:
      at=0                                                                    # Set atom counter, updated geometry
    if N!=None and at!=None and at!=N:                                        # Read atom positions
      if 'Species' in line:                                                   # initital geometry
        at += 1
        atoms.append(line.split()[-4:])
      if 'atom ' in line:                                                     # updated geometry
        at += 1
        aux=append(line.split()[-1],line.split()[-4:-1])
        atoms.append(aux)
atoms=reshape(atoms,[i_step,N,4])
outfile=''
for i in range(i_step):
  outfile=outfile+"          "+str(N)+'\n\n'
  for j in range(N):
    outfile=outfile+"          ".join(atoms[i,j,:])+'\n'
print(outfile)



