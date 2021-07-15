import math
import matplotlib.pyplot as plt
import numpy as np
from random import randint

# import modules from the effmass package
from effmass import inputs, analysis, extrema, outputs, dos, ev_to_hartree


#random_int= randint(10000,99999)
random_int = 'test3' # use this command to specific fig name

#file=open("effmass_test2.txt",'a')

settings = inputs.Settings(extrema_search_depth=0.05, energy_range=0.6)
which_values = ["parabolic m* (least squares)","parabolic m* (finite difference)"]

data = inputs.DataAims("./mode0")
    #use  .format()  can add variable in string
ttt = extrema.find_extrema_indices(data, settings)
my_array=np.concatenate((ttt[0],ttt[1]))
print(my_array)
#print(ttt)
#segments = extrema.generate_segments(settings,data,bk=[[6, 99],[6, 199],[6, 299]])
segments = extrema.generate_segments(settings,data,bk=[[6, 0],[6, 100],[6, 200],[7, 0],[7, 100],[7, 200]])
#print(extrema_array)
for seg in segments:

    print(seg)
#outputs.plot_segments(data,settings,segments)
table=outputs.make_table(segments,which_values)
outputs.print_terminal_table(table)
outputs.plot_segments(data,settings,segments,savefig=True,random_int=random_int)
plt.show()
#file.write(table.get_string())
#file.write('\n')



#print(segments[-1].band)
#cbm_index = segments[-1].band
'''
Here I use band index to determine CBM and VBM. Band index stored in function: segments.band
Here I choose the last band in segment (e.i. segments[-1]), it's index should be CBM
Then I write the loop below to select VBM and CBM from all segments.
'cbm_index - 1' is obviously VBM
'''
#plot_segments = []
#for seg in segments:
#    if seg.band == (cbm_index - 1) or seg.band == (cbm_index):
#        plot_segments.append(seg)
#file.write('{}th effective mass\n'.format(i))

#plot_segments = []
#plot_segments = segments[-6:]

#outputs.plot_segments(data,settings,plot_segments,savefig=True,random_int=random_int)
'''
Attention: Here only plot segment list in 'plot_segments', whcih means only VBM and CBM
'''
#plt.show()
