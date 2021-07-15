import math
import os
import matplotlib.pyplot as plt
import numpy as np
from random import randint

# import modules from the effmass package
from effmass import inputs, analysis, extrema, outputs, dos, ev_to_hartree

file=open("effmass_VBCB.txt",'a')
file.write("material  particle  band-index  direction  Finite difference  Least squares\n")
settings = inputs.Settings(extrema_search_depth=0.03, energy_range=0.3)
which_values = ["parabolic m* (least squares)","parabolic m* (finite difference)"]
random_int = 'test2'

workpath='./'

allfile = os.listdir(workpath)

for files in allfile:

    filepath = "./" + files
    if os.path.isdir(filepath):

        material = files.split('_')[2]


        effmass_path = filepath + "/02_calc_q_ZPR/q1/mode0"


        data = inputs.DataAims(effmass_path)
        segments = extrema.generate_segments(settings,data)
        outputs.plot_segments(data,settings,segments)
        table=outputs.make_table(segments,which_values)
        outputs.print_terminal_table(table)
#        file.write(segment)
#        file.write('\n')
        cbm_index = segments[-1].band
        plot_segments = []
        for seg in segments:
            if seg.band == (cbm_index):
                if seg.band_type == 'conduction_band':
                    particle = "electron"
                if seg.band_type == 'valence_band':
                    particle = "hole"
                plot_segments.append(seg)

        
        file.write("%s  %s  %d  %s  %.4f  %.4f\n" %(material,particle,plot_segments[0].band,plot_segments[0].direction,plot_segments[0].finite_difference_effmass(),plot_segments[0].five_point_leastsq_effmass()))

file.close()
