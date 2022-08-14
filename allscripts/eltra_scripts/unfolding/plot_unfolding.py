import numpy as np
import matplotlib.pyplot as plt
import sys
from matplotlib.lines import Line2D


#colors_flat[:,i] = Color[i]


# FIXME: now only read one k-path, can extand to all k-paths by loop.
def get_kpath_info(unfold_file, control_in):
    f = open(unfold_file,"r")
    i=0
    a=0
    b=0
    #kpoint = []

    # Attention: reciprocal lattice vectors are row vectors!!!
    pc_inv_lv = np.zeros((3,3))
    sc_inv_lv = np.zeros((3,3))
#    print(pc_inv_lv)
    while True:
        band = f.readline()
        i+=1

        if i > 10:
            break
        if 1 < i < 5:

            values = band.split()
            print(values[4:7])
            pc_inv_lv[a,:] =  list(map(float,values[4:7]))
    #        print(pc_inv_lv)
            a+=1
    #        sc_inv_lv =
    #    a=0
        if 5 < i < 9 :
             values = band.split()
             sc_inv_lv[b,:] =  list(map(float,values[4:7]))
             b+=1
        if i == 9:
            values = band.split()
            sc_kps = int(values[1])
            pc_kps = int(values[4])
            n_states = int(values[7])

#    print(pc_inv_lv)
#    print(sc_inv_lv)

    f.close()
    f2 = open(control_in,"r")
    for line in f2:
        words = line.split("#")[0].split()
        nline = " ".join(words)
        if nline.startswith("output band "):
            start = np.array(list(map(float,words[2:5])))
            end = np.array(list(map(float,words[5:8])))
            # Cartesian coordinate K = Frac_coordinate * inv_LV
            length = np.linalg.norm(np.dot(end, pc_inv_lv) - np.dot(start,pc_inv_lv))
    f2.close()
#    print(length)

    return pc_inv_lv, sc_inv_lv, start, length, pc_kps, sc_kps, n_states


def get_all_bands(unfold_file, pc_inv_lv, start, length, pc_kps, sc_kps, n_states):
    # band_info is a 3D array:
    # band_info(each energy eigenstate, each k-point, (k-point coordinate, energy eigenvalue, weight))
    # Currently, it's 5 Column. But it will become 6 Column after calculate distance for x-axis ploting.
    # All 6 columns are: (k-point coordinate, energy eigenvalue, weight, distance_k_to_start)
    qp = int(pc_kps / sc_kps)
    band_info = np.zeros((n_states,qp,sc_kps,5))

    b = 0
    f = open(unfold_file,"r")

    a = 0
    c = 0
    # First 9 lines are not unfolding weights, skip [9:]
    for line in f.readlines()[9:]:
        values = line.split()
        band_info[a,b,c,0:3] = list(map(float,values[1:4]))
        band_info[a,b,c,3:5] = list(map(float,values[7:9]))
        a+=1
        if (a % n_states) == 0:
            a = 0
            b+=1
        if b+1 > qp:
            b = 0
            c+=1

    f.close()
#####################   add distance   ###############################

#    band_info = np.append(band_info, np.zeros((n_states,qp,sc_kps,1)), axis=3)
#    for i in range(qp):
#        for j in range(sc_kps):
#            coord_k = np.dot(band_info[0,i,j,0:3], pc_inv_lv)
#            distance = np.linalg.norm(np.dot(start, pc_inv_lv)-coord_k)
#            band_info[:,i,j,5] = distance
######################################################################
#    print('qp_1 state_1: \n',band_info[0,0,:,:])
    print(np.shape(band_info))
    return band_info, qp


def determine_unfolded_path(band_info, qp, sc_kps):
    # One supercell k-path may map to multiple different primitive cell k-paths after unfolding
    # In this subroutine: judge collinearation by cross product = 0 for three kpoints,
    # divide kpoints into several non-collinear segments and plot separately.
    precision = 1e-6
    segment_count = []
    names = globals()
    for iq in range(qp):
        print('iq', iq)
        names['frac_k_qp'+str(iq)] = band_info[0,iq,:,0:3]
#    print(frac_k_qp0)
    for iq in range(qp):
        count = 0           # each q-point have how many non-collinear segments
        new_start = 0
        edge1 = names['frac_k_qp'+str(iq)][1,:] - names['frac_k_qp'+str(iq)][new_start,:]
    #    names['band_qp0_'+str(count)] = band_info[:,0,new_start:2,:]
        for i in range(2,sc_kps):

            edge2 = names['frac_k_qp'+str(iq)][i,:] - names['frac_k_qp'+str(iq)][new_start,:]
            cross_prd = np.linalg.norm(np.cross(edge1, edge2))
#            print(i, ' ',cross_prd)
            if cross_prd < precision:
    #            print('count: ',count)
                names['band_qp'+str(iq)+'_'+str(count)] = band_info[:,iq,new_start:i+1,:]
            if cross_prd >= precision:
                new_start = i
                count += 1
                if len(names['frac_k_qp'+str(iq)][new_start:,0]) == 1:
                    names['band_qp'+str(iq)+'_'+str(count)] = band_info[:,iq,new_start:,:]
                else:
                    edge1 = names['frac_k_qp'+str(iq)][new_start,:] - names['frac_k_qp'+str(iq)][new_start+1,:]
        # segment_count: number of non-colinear kpath in each q-point. Start counting from 1 not 0.
        segment_count = np.append(segment_count, int(count+1))
        segment_count = np.array(segment_count, dtype='int32')
#    print(np.shape(band_qp1_0[0,:,:]), np.shape(band_qp1_1[0,:,:]))
#    print(band_qp1_0[0,:,:])
    print('count: ', segment_count[1])
    nocol_list = np.arange(segment_count.sum())
    print(nocol_list)
    ii = 0
    for iq in range(qp):
        for jj in range(segment_count[iq]):
            names['band_fin_'+str(ii)] =  names['band_qp'+str(iq)+'_'+str(jj)]
            ii += 1
    print(ii)
    # ii: number of temporary band segments
    t = 0
    colinear_nr = []
    single_point = []
    # colinear_nr store colinear band segments, if i in range(ii) coincide these nr. jump to next loop.
    # e.g. [0,1,2,3,4,5] 6 band segments, 0,1,2 are colinear. Then we only need to merge 01 and 02, we can jump loop of segment 1 and 2.
    # in this case colinear_nr = [1,2]
    for i in range(ii):
        if i in colinear_nr:
            continue



        for j in range(i+1,ii):
            if len(names['band_fin_'+str(i)][0,:,0]) == len(names['band_fin_'+str(j)][0,:,0]) == 1:
                continue
            if len(names['band_fin_'+str(i)][0,:,0]) == 1:

                edge3 = names['band_fin_'+str(j)][0,1,0:3] - names['band_fin_'+str(j)][0,0,0:3]
                edge4 = names['band_fin_'+str(i)][0,0,0:3] - names['band_fin_'+str(j)][0,1,0:3]
            else:
                edge3 = names['band_fin_'+str(i)][0,1,0:3] - names['band_fin_'+str(i)][0,0,0:3]
                edge4 = names['band_fin_'+str(j)][0,0,0:3] - names['band_fin_'+str(i)][0,1,0:3]
            cross_prd = np.linalg.norm(np.cross(edge3, edge4))
            if cross_prd < precision:
                print('merge colinear band: band_fin_'+str(i)+' and band_fin_'+str(j) )
                names['band_fin_'+str(i)] = np.append(names['band_fin_'+str(i)], names['band_fin_'+str(j)], axis = 1)
                dele_nr = j - t
                colinear_nr = np.append(colinear_nr,j)
                nocol_list = np.delete(nocol_list, dele_nr)
                t += 1

    print('nocol_list: ',nocol_list)
#    print(np.shape(band_fin_0), np.shape(band_fin_1), np.shape(band_fin_2))

    # Output
    t = 0
    kp_list = []
    for i, val in enumerate(nocol_list):
        num_kp = np.size(names['band_fin_'+str(val)][0,:,0])
        if num_kp == 1:
            print('delete single point path: ',names['band_fin_'+str(val)][0,0,0:3])
            dele_nr2 = val - t
            nocol_list = np.delete(nocol_list, dele_nr2)
            t += 1

        if num_kp > 1:
            kp_list = np.append(kp_list, num_kp)
            kp_list = np.array(kp_list, dtype='int32')
    print('kp_list: ',kp_list)
    band_out = names['band_fin_'+str(nocol_list[0])]
    for i in range(1, np.size(nocol_list)):
        band_out = np.append(band_out, names['band_fin_'+str(nocol_list[i])], axis = 1)
    print(np.shape(band_out))
    # Above we have colinear segments in each q-point, below will judge colinearity across different q-points

#     no_col = 0
#     for iq in range(qp):
#     # loop of every qp: in this first qp, compare each k-path with k-paths in other qp(i.e. below iq+ii and count2)

#         for count in range(segment_count[iq]):
#             names['band_fin_'+str(no_col)] = names['band_qp'+str(iq)+'_'+str(count)]
#             # k-paths in the 'first' qp
#             edge3 = names['band_qp'+str(iq)+'_'+str(count)][0,1,0:3] - names['band_qp'+str(iq)+'_'+str(count)][0,0,0:3]
#             for ii in range(1,qp+1):
#                 # compare with k-path in other qp, iq+ii make sure we only compare with larger qp, avoid double-counting.
#                 if iq + ii < qp:
#                     # this conditional expression (if) is for avoidng out of range.
#                     print('iq: ', iq , "ii", ii)
#                     for count2 in range(segment_count[iq+ii]):
#                         edge4 = names['band_qp'+str(iq+ii)+'_'+str(count2)][0,0,0:3] - names['band_qp'+str(iq)+'_'+str(count)][0,1,0:3]
#                         # whether these k-paths between different qp are colinear
#                         cross_prd = np.linalg.norm(np.cross(edge3, edge4))
#                         if cross_prd < precision:
#                             # if so, merge colinear paths.
#                             print('merge colinear band: band_qp'+str(iq)+'_'+str(count)+' and band_qp'+str(iq+ii)+'_'+str(count2) )
#                             names['band_fin_'+str(no_col)] = np.append(names['band_qp'+str(iq)+'_'+str(count)], names['band_qp'+str(iq+ii)+'_'+str(count2)], axis = 1)
#                             #no_col +=1
#                         else:
#                             no_col += 1
#                             names['band_fin_'+str(no_col)] = names['band_qp'+str(iq+ii)+'_'+str(count2)]
#         no_col += 1
#     print(np.shape(band_fin_0), np.shape(band_fin_1), np.shape(band_fin_2))
#     print(no_col)
    return kp_list, band_out


def unfold_band_segments(band_info, n_states, pc_kps, sc_kps):

    n_qpoint = int(pc_kps / sc_kps)
    names = globals()
    for i_qpoint in range(n_qpoint):
        print('strL ', str(i_qpoint))
        names['band_qp_'+str(i_qpoint)] = np.zeros((n_states,sc_kps,6))
        print(band_qp_0)
    for i in range(pc_kps):
        qp = i % n_qpoint
        names['band_qp_'+str(qp)] = np.append(names['band_qp_'+str(qp)],band_info[:,i,:])
    print('band_qp_1: \n',band_qp_1[0,:,:])




def flatten_points(band_out, kp_list, n_states, pc_inv_lv, length, Color):
    # Prepare for plot, including calculate x axis, color scale and flatten to 1d array.
    # FIXME: We may drop out some kpoints (at ends of k-path) when ploting. It's fixable, I think.
    pc_kps = np.sum(kp_list)
    print('pc_kps', pc_kps)
    # Calculate x axis(distance) for each k-path
    band_out = np.append(band_out, np.zeros((n_states,pc_kps,1)), axis=2)
    #print('band out(flatten_points)', band_out[0,0:32,:])

    # Find start point for each k-path:
    start = 0
    distance_start = 0
    space = 1.15
    boundary_points = []
    for nr_path, num_k in enumerate(kp_list):
#        Here num_k is number of kpoints in each k-path
#        print(nr_path, i)
        start_p = np.argmin(band_out[0, start:start+num_k,0:3], axis = 0)
#         print('band_out[0,:,:] \n',band_out[0, start:start+i,0:3])
        end_p = np.argmax(band_out[0, start:start+num_k,0:3], axis = 0)
        t = 0
        for j in range(3):
            if band_out[0,start,j] == band_out[0,start+1,j] and band_out[0,start,j] == band_out[0,start+2,j] and band_out[0,start,j] == band_out[0,start+(num_k-1),j]:
                dele_nr = j - t
                start_p = np.delete(start_p, dele_nr)
                end_p = np.delete(end_p, dele_nr)
                t += 1
        unique_start, count_start = np.unique(start_p, return_counts = True)
        unique_end, count_end = np.unique(end_p, return_counts = True)
        print('Start point of k-path nr.',nr_path,'is', band_out[0,start+unique_start[0],0:3])
        print('K-path nr.',nr_path,'is',band_out[0,start+unique_start[0],0:3], '--->', band_out[0,start+unique_end[0],0:3] )


        start_coord = np.dot(band_out[0,start+unique_start[0],0:3], pc_inv_lv)
        end_coord = np.dot(band_out[0,start+unique_end[0],0:3], pc_inv_lv)
        length = np.linalg.norm(start_coord -end_coord)
        for ii in range(num_k):

            coord_k = np.dot(band_out[0,start+ii,0:3], pc_inv_lv)
            distance = distance_start + np.linalg.norm(start_coord - coord_k)
            band_out[:,start+ii,5] = distance
#         print('count: ',unique, count)
#             elif start_p[0] == start_p[1] or start_p[0] == start_p[2]:
#                start_k = band_out[0,start_p[0],0:3]
#             elif start_p[0] == start_p[1] or start_p[0] == start_p[2]:
#                start_k = band_out[0,start_p[0],0:3]
        boundary_points = np.append(boundary_points, band_out[0,start+unique_start[0],5])
        boundary_points = np.append(boundary_points, band_out[0,start+unique_end[0],5])
        distance_start += space*length
        start += num_k
#         print('Start point nr.', nr_path,'is: ', start_p )
#     for j in range(pc_kps):
#         coord_k = np.dot(band_out[0,j,0:3], pc_inv_lv)
#         distance = np.linalg.norm(np.dot(start, pc_inv_lv)-coord_k)
#         band_out[:,j,5] = distance
#    print(band_out[0,:,:])
    # color array
    print(np.shape(band_out))
    color_flat = np.zeros((n_states*pc_kps, 4))
    for i in range(3):
        color_flat[:,i] = Color[i]
    color_flat[:,3] = band_out[:,:,4].flatten()
    kp_flat = band_out[:,:,5].flatten()
    eval_flat = band_out[:,:,3].flatten()
    print('color, kp and eval shapes', np.shape(color_flat),np.shape(kp_flat),np.shape(eval_flat))
    return color_flat, kp_flat, eval_flat, boundary_points



def plot_band(color_flat, kp, evals, boundary, plot_name):

    fig = plt.scatter( kp, evals,linestyle="None",marker='x',label='solution',color=color_flat, s=10)
    print('boundaries: ', boundary)
    boundary = np.delete(boundary, -1)
    boundary = np.delete(boundary, 0)
    print(boundary)
    for xpos in boundary:
        plt.axvline(xpos,color='gray',linestyle=":")
    plt.xlim(0,max(kp))
    plt.xticks([])
    plt.ylim(-23,23)
    plt.savefig(plot_name, dpi = 250)

    plt.show()

def plot_2spectrum(color_flat1, kp1, evals1, boundary, color_flat2, kp2, evals2, plot_name):

    #fig = plt.scatter( kp, evals,linestyle="None",marker='x',label='solution',color=color_flat, s=10)
    fig, ax = plt.subplots()
    ax.scatter(kp1, evals1,linestyle="None",marker='x',label='solution',color=color_flat1, s=10)
    ax.scatter(kp2, evals2,linestyle="None",marker='x',label='solution',color=color_flat2, s=10)
    print('boundaries: ', boundary)
    boundary = np.delete(boundary, -1)
    boundary = np.delete(boundary, 0)
    print(boundary)
    for xpos in boundary:
        plt.axvline(xpos,color='gray',linestyle=":")
    plt.xlim(0,max(kp1))
    plt.xticks([])
    plt.ylim(13,23)
    plt.savefig(plot_name, dpi = 250)

    plt.show()

def cut_spectrum(unfold_file, specific_spectrum, next_spectrum, spectrum1, spectrum2):
    #qp = int(pc_kps / sc_kps)
    #band_info = np.zeros((n_states,qp,sc_kps,5))
    #unfold_info = []
    i = 0
    str1 = ' '
    f = open(unfold_file,"r")
    f1 = open(spectrum1, "w")
    f2 = open(spectrum2, "w")

    while True:
        line = f.readline()
        i+= 1

        if i <=8:
            f1.write(line)
            #f1.write('\n')
            f2.write(line)
            #f2.write('\n')

        if i ==9:
            unfold_info = line.split()
            print('line: ', type(line), line)
            print('unfold_info: ', type(unfold_info), unfold_info)
            unfold_info[7] = str(specific_spectrum)
            f1.write(str1.join(unfold_info))
            f1.write('\n')
            unfold_info[7] = str(next_spectrum)
            f2.write(str1.join(unfold_info))
            f2.write('\n')
        if i > 9:
            values = line.split()
            #print(values)
            if values == []:
                break
            if int(values[6]) > specific_spectrum:
                f2.write(line)
            elif int(values[6]) <= specific_spectrum:
                f1.write(line)


    f1.close()
    f2.close()

    f.close()





# MAIN routine:
unfold_file = 'full_band_unfold_1.out'
control_in = 'full_control.in'
save_name = 'testing.png'
print("Start ")
pc_inv_lv, sc_inv_lv, kpath_start, length, pc_kps, sc_kps, n_states = get_kpath_info(unfold_file, control_in)
print(pc_inv_lv)
print('sc_kps: ',sc_kps,'pc_kps: ',pc_kps,'n_states: ',n_states, 'length: ', length)
band_info, qp = get_all_bands(unfold_file, pc_inv_lv, kpath_start, length, pc_kps, sc_kps, n_states)
#unfold_band_segments(band_info, n_states, pc_kps, sc_kps)
kp_map, band_out = determine_unfolded_path(band_info, qp, sc_kps)

ColorOrange = np.array(  ( 255.0/255.0 ,  127.0/255.0 ,  14.0/255.0 ) )
ColorBlue = np.array(  ( 30.0/255.0 ,  144.0/255.0 ,  255.0/255.0 ) )
#flatten_points(band_out, kp_map, n_states, pc_inv_lv, length, ColorOrange)
color_flat, kp_flat, eval_flat, boundary_points = flatten_points(band_out, kp_map, n_states, pc_inv_lv, length, ColorOrange)
plot_band(color_flat, kp_flat, eval_flat, boundary_points, save_name)

#### plot multiple spectrums ###

specific_spectrum = 10
next_spectrum = 10
spectrum1 = 'band_unfold_spectrum1.out'
spectrum2 = 'band_unfold_spectrum2.out'
plot_name = 'test_spectrum_13_23.png'

#cut_spectrum(unfold_file, specific_spectrum, next_spectrum, spectrum1, spectrum2)
pc_inv_lv_1, sc_inv_lv_1, kpath_start_1, length_1, pc_kps_1, sc_kps_1, n_states_1 = get_kpath_info(spectrum1, control_in)
band_info_1, qp_1 = get_all_bands(spectrum1, pc_inv_lv_1, kpath_start_1, length_1, pc_kps_1, sc_kps_1, n_states_1)
kp_map_1, band_out_1 = determine_unfolded_path(band_info_1, qp_1, sc_kps_1)
color_flat_1, kp_flat_1, eval_flat_1, boundary_points_1 = flatten_points(band_out_1, kp_map_1, n_states_1, pc_inv_lv_1, length_1, ColorOrange)

pc_inv_lv_2, sc_inv_lv_2, kpath_start_2, length_2, pc_kps_2, sc_kps_2, n_states_2 = get_kpath_info(spectrum2, control_in)
band_info_2, qp_2 = get_all_bands(spectrum2, pc_inv_lv_2, kpath_start_2, length_2, pc_kps_2, sc_kps_2, n_states_2)
kp_map_2, band_out_2 = determine_unfolded_path(band_info_2, qp_2, sc_kps_2)
color_flat_2, kp_flat_2, eval_flat_2, boundary_points_2 = flatten_points(band_out_2, kp_map_2, n_states_2, pc_inv_lv_2, length_2, ColorBlue)

plot_2spectrum(color_flat_1, kp_flat_1, eval_flat_1, boundary_points, color_flat_2, kp_flat_2, eval_flat_2, plot_name)
