#!/home/quan/anaconda3/bin/python

import math
import matplotlib.pyplot as plt
import numpy as np

# import modules from the effmass package
from effmass import inputs, analysis, extrema, outputs, dos, ev_to_hartree




file=open("../all_effmass.txt",'a')

settings = inputs.Settings(extrema_search_depth=0.03, energy_range=0.3)
which_values = ["parabolic m* (least squares)","parabolic m* (finite difference)"]

for i in range(0,7):

    data = inputs.DataAims("./mode{}".format(i))
    #use  .format()  can add variable in string

    segments = extrema.generate_segments(settings,data)
    outputs.plot_segments(data,settings,segments)
    table=outputs.make_table(segments,which_values)
    outputs.print_terminal_table(table)
    file.write('{}th effective mass\n'.format(i))
    file.write(table.get_string())
    file.write('\n')
#plt.show()
