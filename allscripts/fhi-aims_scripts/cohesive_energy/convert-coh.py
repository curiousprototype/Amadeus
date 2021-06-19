#!/usr/bin/python
import numpy as np
from optparse import OptionParser

#main
if __name__ =='__main__':

  parser = OptionParser()
  parser.add_option("-i", help="total energy file", action="store",
                    dest="eTotalFile", type=str)
  parser.add_option("-o", help="cohesive energy file", action="store",
                    dest="eCohFile", type=str)
  parser.add_option("--nAtoms", help="number of atoms in sc cell", action="store",
                    dest="nAtoms", type=int)
  parser.add_option("--eAtom", help="total energy of single atom", action="store",
                    dest="eAtom", type=float)

  (options,args) = parser.parse_args()
  
  # Write cohesive energy
  filename = options.eCohFile
  fout = open(filename,'w')
  fout.write("# %-14s %-14s\n" % ("V [A^3]","E_coh [eV]"))
  
  filename = options.eTotalFile
  fin = open(filename,'r')
  
  for line in fin:
    data = line.split()
    if (data[0] != "#"):
      aLat = float(data[0])
      eTot = float(data[1])

      vol  = aLat**3 / options.nAtoms
      eCoh = eTot - options.eAtom
   
      fout.write("%14.6f %14.6f\n" % (vol,eCoh))
  
  # Close file
  fin.close()
  fout.close()
