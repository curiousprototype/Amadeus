import numpy as np

file = open('data.csv')
file_write = open('overalldata.csv', 'w')
i = 0
list_x = []
list_y = []

# read line by line from output file
while True:
    text = file.readline()
    i += 1
    if not text:
        break

    #cut useful data from the whole file

    if  i >=1 and i <=39:

        list_examp = text.split(',')
        list_new = []
        for ii, val in enumerate(list_examp):
           # newii = ii.strip(',')
             if (ii==0 or ii==1 or ii==3 or ii==4 or ii==5 or ii==6 or ii==7 or ii==8 or ii==9 or ii==13 or ii==19 or ii==23 or ii==25 or ii==26 or ii==27 or ii==29):
                 list_new.append(val)
##            list_new.append(ii)
#        print(list_new)
        str_write = ",".join(list_new)
        file_write.write(str_write)
        file_write.write('\n')

file.close()
file_write.close()

