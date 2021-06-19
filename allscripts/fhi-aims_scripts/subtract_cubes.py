#Subtracts cube file 1 from 2 and writes in file 3. Keeps header from the first file.

from sys import argv

f = open(argv[1])
g = open(argv[2])
z = open(argv[3], 'w')

for i in f:
 if len(i.split()) == 6:
  break
 z.write(i)

for j in g:
 if len(j.split()) == 6:
  break

tmp = [z.write('% .5E ' % (k-l)) for k,l in zip(list(map(float, i.split())), list(map(float, j.split())))]
z.write('\n ')

for i,j in zip(f,g):
  tmp = [z.write('% .5E ' % (k-l)) for k,l in zip(list(map(float, i.split())), list(map(float, j.split())))]
  z.write('\n ')

z.close()

