# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 21:40:44 2018

@author: edmon_000
"""

from sklearn.cluster import DBSCAN
from sklearn import metrics
import editdistance
import numpy as np
import scipy.spatial.distance as spt
import matplotlib.pyplot as plt
import kmediods as kmedoids
import re
import os



# uses the TKS algorithm k = 5000 or k=1000

num = 7


project_dir = 'C:/Users/edmon_000/Desktop/mldmyear2/mldm project/spmf/output/'
file = project_dir + "output_"+str(num)
key = ""

output_dir = project_dir + str(num) + "/"

seq = []


def get_num_patterns(file=file):
    with open(file) as f:
        lcount = 0
        for line in f:
            lcount += 1
    return lcount


pattern_indices = np.empty(get_num_patterns(),dtype=object)

def get_pattern_index_list (ind):
    el =  re.findall('\d+', ind)
    el = [*map(int, el)]
    return el

with open(file ) as f:
    index = 0
    for line in f:
        #inner_list = [elt.strip() for elt in line.split(',')]
        # in alternative, if you need to use the file content as numbers
        # inner_list = [int(elt.strip()) for elt in line.split(',')]
        # list_of_lists.append(inner_list)
        
        ind_sup_label = line.index("#SUP:")
        ind_sid_label = line.index("#SID:")
        
        seq.append(line [0:ind_sup_label].replace("-1","").replace(" ", ""))
        pattern_indices[index] = get_pattern_index_list(line[ind_sid_label+5:])
       # pattern_indices[index] = line[ind_sup_label+5:]
        index += 1
        
def lev_metric(x, y):
    i, j = int(x[0]), int(y[0])     # extract indices
    d = editdistance.eval(seq[i], seq[j])
    return d

def get_distance_matrix(seq):
    
    alldist = np.zeros((len(seq),len(seq)))
    i = 0
    for el in seq:
        j = 0
        for el2 in seq:
              alldist[i-1,j-1] = editdistance.eval(el,el2)
              j += 1
        i += 1
    #print(str(i)+" "+str(j))
    #alldist = np.reshape(alldist,len(seq), len(seq))          
    return alldist

#X = np.arange(len(seq)).reshape(-1, 1)
X = get_distance_matrix(seq)

C,M,mediods = kmedoids.kMedoids(X,6) 
for mm in mediods:
    print (seq[mm])


np.save(output_dir + key  + str(num)+ "_X",X)
np.save(output_dir + key  + str(num)+ "_M",M)
np.save(output_dir + key  + str(num)+ "_C",C)
np.save(output_dir + key  + str(num)+ "_mediods",mediods)
np.save(output_dir + key  + str(num)+ "_pattern_indices",pattern_indices)
np.save(output_dir + key  + str(num)+ "_seq",seq)



#cluster =  DBSCAN(metric='precomputed', eps=5, min_samples=1).fit(X)
#cluster_labels = cluster.labels_
#y = list(np.where(cluster_labels==0))

