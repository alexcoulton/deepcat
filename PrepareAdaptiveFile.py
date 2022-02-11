#! usr/bin/python

import os
from os.path import exists
import numpy as np
import csv
from csv import reader
import sys
import pdb

indir=sys.argv[1]
outdir=sys.argv[2]

try:
    if(sys.argv[3] == 'r1'):
        version1 = True
except:
    version1 = False
    
thr=10000

#def PrepareAdaptiveFile(indir,outdir,thr=10000):
ffs=os.listdir(indir)



count1 = 1
for ff in ffs:
    if(version1):
        aa_row = 53
        freq_row = 58
        vmax_row = 96
    else:
        aa_row = 1
        freq_row = 3
        vmax_row = 5

    print('count1 = ' + str(count1))
    if('.tsv' not in ff):  
       continue
    ff0=ff
    if not os.path.exists(outdir):
       os.makedirs(outdir)   
    str1='TestReal-'   
    newff=outdir+'/'+str1+ff0
#    if exists(newff)==False:
#       continue
    csv_reader = reader(open(indir+'/'+ff,"r"), delimiter='\t', quotechar="\"") 
    ddnew=[] 
    for row in csv_reader:
      if '*' not in row[aa_row]:
        # print(row[aa_row])
        if 'X' not in row[aa_row]:
#         if '^C.+F$' not in row[aa_row]:
          if (len(row[aa_row])>=10) and (len(row[aa_row])<=24):
            # print('len(row(aa_row))')
            # print(len(row[aa_row]))
            if 'unresolved' not in row[vmax_row]:
              # print(row[vmax_row])
              if (row[aa_row][0]=='C') and (row[aa_row][-1]=='F'):
                  ddnew.append(row)

    def select(x):
        indices1 = [aa_row, freq_row, vmax_row]
        return map(x.__getitem__, indices1)

    # pdb.set_trace()
    if(len(ddnew) == 0):
        print('skip')
        count1 += 1
        continue

    #subset the ddnew array to only include columns of interest
    ddnew = [list(select(x)) for x in ddnew]

    aa_row = 0
    freq_row = 1
    vmax_row = 2

    ddnew=np.array(ddnew)      
    sorted_array = ddnew[ddnew[:,freq_row].astype(float).argsort()]   
    reverse_array = sorted_array[::-1]

    if len(reverse_array)>thr:
       col1=reverse_array[0:thr,aa_row]
       col2=reverse_array[0:thr,vmax_row]
       col3=reverse_array[0:thr,freq_row]
    else:
       col1=reverse_array[:,aa_row]
       col2=reverse_array[:,vmax_row]
       col3=reverse_array[:,freq_row]
    c=zip(col1,col2,col3)
    first_row='amino_acid	v_gene	frequency'
    f=open(newff, 'w')
    f.write(first_row)
    f.write('\n')
    f.close()
    count1 += 1
    with open(newff, 'w') as f:
       writer = csv.writer(f, delimiter='\t')
       writer.writerows(c)
