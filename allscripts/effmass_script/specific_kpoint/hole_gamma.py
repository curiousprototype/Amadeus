import math
import os
import matplotlib.pyplot as plt
import numpy as np
from random import randint

# import modules from the effmass package
from effmass import inputs, analysis, extrema, outputs, dos, ev_to_hartree

file=open("hole_gamma.txt",'a')
file.write("Gamma-point\n")
file.write("material  particle  band-index  direction  Finite difference  Least squares\n")
settings = inputs.Settings(extrema_search_depth=0.03, energy_range=0.3)
which_values = ["parabolic m* (least squares)","parabolic m* (finite difference)"]
random_int = 'test2'

workpath='./'

allfile = os.listdir(workpath)

for files in allfile:

    filepath = "./" + files
    if os.path.isdir(filepath):

        material = files.split('_')[2]        # get material name by split dir name


        effmass_path = filepath + "/02_calc_q_ZPR/q1/mode0"


        data = inputs.DataAims(effmass_path)
        segments = extrema.generate_segments(settings,data)
        outputs.plot_segments(data,settings,segments)
        table=outputs.make_table(segments,which_values)
        outputs.print_terminal_table(table)
#        file.write(segment)
#        file.write('\n')
        cbm_index = segments[-1].band

# calculate effective mass at Gamma Point
# in order to specify the k-position of effmass(such as Gamma point), we need to set argument 'bk' 
# such as bk=[[4, 0],[4, 100],[4, 200]] at 'extrema.generate_segments()'
# Here I write a loop to generate this bk array
        vbm_index = cbm_index - 1
        k_point = 0                  # Gamma-point
        seg_position = []            # array of one single segment e.g. [4, 0]
        all_segs = []                # array of all segments e.g. [[4, 0],[4, 100],[4, 200]]
        for i in range(3):
            seg_position = []       
            seg_position.append(vbm_index)
            seg_position.append(k_point)           # write one segment array
            all_segs.append(seg_position)          # append each segment into all segments array
            k_point += 100           # Gamma-point of all three band k-path

        gamma_segments = extrema.generate_segments(settings,data,bk=all_segs)  # bk = all_segs

        plot_segments = []
        for seg in gamma_segments:
            if seg.band == (vbm_index):               #  only print vbm band (hole effectivemass)
                if seg.band_type == 'conduction_band':
                    particle = "electron"
                if seg.band_type == 'valence_band':
                    particle = "hole"
                plot_segments.append(seg)



        
        file.write("%s  %s  %d  %s  %.4f  %.4f\n" %(material,particle,plot_segments[0].band,plot_segments[0].direction,plot_segments[0].finite_difference_effmass(),plot_segments[0].five_point_leastsq_effmass()))

file.close()
