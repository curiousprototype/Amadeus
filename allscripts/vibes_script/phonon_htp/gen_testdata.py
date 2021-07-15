import numpy as np

file = open('data.csv')
#file_write = open('data.csv', 'w')
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
    
    if  i >=2 and i <=139:
        
        list_examp = text.split(',')
        list_new = []
        result1 = float(list_examp[5]) * float(list_examp[22]) * float(list_examp[6])
        result2 = (float(list_examp[15]) / float(list_examp[14])) + float(list_examp[5])
        result3 = result1 / result2
        print(result3)
#        for ii, val in enumerate(list_examp):

           # newii = ii.strip(',')


           #  if not (ii==26):
#                 list_new.append(val)
##            list_new.append(ii)
#        print(list_new)
#        str_write = ",".join(list_new) 
#        file_write.write(str_write)
#        file_write.write('\n')

file.close()
file_write.close()
