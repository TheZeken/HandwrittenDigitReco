#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 19:05:03 2017

@author: mathieu
"""

import numpy as np

#print("freeman_chain = ",freeman_chain)

def levenshtein(chaine1, chaine2):
    
    dist = np.zeros((len(chaine1)+1,len(chaine2)+1))
    for i in range(len(chaine1)+1):
        dist[i, 0] = i
    for j in range(len(chaine2)+1):
        dist[0, j] = j
    for i in range(1,len(chaine1)+1):
        for j in range(1,len(chaine2)+1):
            if chaine1[i-1] == chaine2[j-1]:
                cost = 0
            elif (chaine2[j-1] - chaine1[i-1]) %8 == 1:
                cost = 0.5
            elif (chaine2[j-1] - chaine1[i-1]) %8 == 2:
                cost = 1
            elif (chaine2[j-1] - chaine1[i-1]) %8 == 3:
                cost = 1.5
            elif (chaine2[j-1] - chaine1[i-1]) %8 == 4:
                cost = 2
            elif (chaine2[j-1] - chaine1[i-1]) %8 == 5:
                cost = 1.5
            elif (chaine2[j-1] - chaine1[i-1]) %8 == 6:
                cost = 1
            elif (chaine2[j-1] - chaine1[i-1]) %8 == 7:
                cost = 0.5
            dist[i,j] = min(dist[i-1, j]+1, dist[i, j-1]+1, dist[i-1, j-1]+cost)
    
    print(dist)
    return dist[len(chaine1),len(chaine2)]

freeman_ex1 = [0,4,2,1,2]
freeman_ex2 = [0,1,0,1,2]            
print(levenshtein(freeman_ex1, freeman_ex2))