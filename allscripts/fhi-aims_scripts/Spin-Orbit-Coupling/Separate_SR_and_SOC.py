#!/usr/bin/python
import os
import shutil

if (os.path.exists("SR") ):
    print("The SR folder already exists, exiting.")
    exit()
if (os.path.exists("SOC") ):
    print("The SOC folder already exists, exiting.")
    exit()

# Create directory
os.makedirs("SR")
os.makedirs("SOC")


# Copy the band*.out files to SOC
for f in os.listdir():
    if (f.startswith("band") and f.endswith("out")):
        shutil.move(f, "SOC")



# Copy the band*.out.no_soc files to SR
for f in os.listdir():
    if (f.startswith("band") and f.endswith("no_soc")):
        shutil.move(f, "SR")

for filename in os.listdir("SR"):
    src = 'SR/' + filename
    (shortname, extension) = os.path.splitext(filename)
    dst = 'SR/' + shortname
    os.rename(src, dst)



print("Separating out SOC calculations")

os.chdir("SOC")
# Copy geometry.in file to SOC
os.system('cp ../geometry.in .')

# To plot the band structures, we need the k-path in a control.in file
os.system('grep "output band" ../control.in >> control.in')

fout1 = open("control.in",'a')
fout1.write("include_spin_orbit non_self_consistent\n")

fout1.close()

# Run $AIMSUTILS/set_band_structure_VBM_to_zero_energy.sh 
os.system("bash $AIMSUTILS/set_band_structure_VBM_to_zero_energy.sh")

#########################################
print("Separating out SR calculations")

os.chdir("../SR")
# Copy geometry.in file to SR
os.system('cp ../geometry.in .')

# To plot the band structures, we need the k-path in a control.in file
os.system('grep "output band" ../control.in >> control.in')

fout2 = open("control.in",'a')

if (os.path.exists("band2001.out") ):
    fout2.write("spin collinear\n")
else:
    fout2.write("spin none\n")

fout2.close()

# Run $AIMSUTILS/set_band_structure_VBM_to_zero_energy.sh 
os.system("bash $AIMSUTILS/set_band_structure_VBM_to_zero_energy.sh")
