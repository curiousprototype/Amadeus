# Amadeus
This folder is a remote back-up for all valuable stuffs in my research and others.

File ***allscripts*** stored all scripts I wrote as a back-up
1. high-throughput scripts using **effmass** code to generate effective masses for many materials.
<br/>**effmass**: https://github.com/lucydot/effmass
2. small bash and python scripts to modify input files and post-process for **SISSO++** code.

3. scripts for **FHI-aims**
<br/>
To compile **FHI-aims**, I recommend to use **Intel oneAPI toolkits** (espacially ifort, icc, imkl and impi).
Here's a cmake file shows flags and compilers I use to compile FHI-aims.
Attention: use ***mpiifort*** and ***mpiicc*** instead of simply ifort or icc because we use MPI.

