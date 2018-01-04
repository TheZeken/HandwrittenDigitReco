#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 19:05:03 2017

@author: mathieu
"""
#%%
#Import data and create histograms
# Database settings to downloads freeman codes
import pymysql
import pymysql.cursors
import pandas as pd
import operator
import numpy as np
import time
import math

#print("freeman_chain = ",freeman_chain)
#%% 
#Remove Nan from a list
# Usefull for Edit Distance
def removeNan(chaine_):
    chaine1 = np.array([]).tolist()
    for i in range(len(chaine_)):
        if math.isnan(int(chaine_[i])):
            break
        else:
            chaine1.append(chaine_[i])
    return chaine1

def levenshtein(string1, string2):
#    print(string1)
    chaine1 = list(string1)
    chaine2 = list(string2)
    
    dist = np.zeros((len(chaine1)+1,len(chaine2)+1))
    for i in range(len(chaine1)+1):
        dist[i, 0] = i
    for j in range(len(chaine2)+1):
        dist[0, j] = j
    for i in range(1,len(chaine1)+1):
        for j in range(1,len(chaine2)+1):
            if int(chaine1[i-1]) == int(chaine2[j-1]):
                cost = 0
            elif (int(chaine2[j-1]) - int(chaine1[i-1])) %8 == 1:
                cost = 1
            elif (int(chaine2[j-1]) - int(chaine1[i-1])) %8 == 2:
                cost = 2
            elif (int(chaine2[j-1]) - int(chaine1[i-1])) %8 == 3:
                cost = 3
            elif (int(chaine2[j-1]) - int(chaine1[i-1])) %8 == 4:
                cost = 4
            elif (int(chaine2[j-1]) - int(chaine1[i-1])) %8 == 5:
                cost = 3
            elif (int(chaine2[j-1]) - int(chaine1[i-1])) %8 == 6:
                cost = 2
            elif (int(chaine2[j-1]) - int(chaine1[i-1])) %8 == 7:
                cost = 1
            dist[i,j] = min(dist[i-1, j]+2, dist[i, j-1]+2, dist[i-1, j-1]+cost)
    
#    print(dist)
    return dist[len(chaine1),len(chaine2)]

#freeman_ex1 = [0,4,2,1,2]
#freeman_ex2 = [0,1,0,1,2]            
#print(levenshtein(freeman_ex1, freeman_ex2))


# Connect to the database.
conn = pymysql.connect(db='ml_db', user='root', passwd='23Octobre', host='localhost')
sql_get_freeman = "SELECT `freeman`,`label` FROM `freeman_number`"
sql_get_distance = "SELECT `dist` FROM `precompute`"
#%%
with conn.cursor() as cursor:
    cursor.execute(sql_get_freeman) #We execute our SQL request
    conn.commit()
    
    df_train = []
    df_test = []
    
    cpt=0
    
    for row in cursor:
        
        if cpt < 600:
            cpt +=1
            values = row[0]
#            print(values)
#            df2 = pd.DataFrame([[values_hist[0]],[values_hist[1]],[values_hist[2]],[values_hist[3]],[values_hist[4]],[values_hist[5]],[values_hist[6]],[values_hist[7]],[row[1]]])
            df_train.append(values)
        elif cpt < 700:
            cpt +=1
            values = row[0]
#            df2 = pd.DataFrame([[values_hist[0]],[values_hist[1]],[values_hist[2]],[values_hist[3]],[values_hist[4]],[values_hist[5]],[values_hist[6]],[values_hist[7]],[row[1]]])
            df_test.append(values)
        else:
            break 
        
    cursor.execute(sql_get_distance) #We execute our SQL request
    conn.commit()
    
    train_dist = {}    
    distance = []
    for row in cursor:
        distance.append(row)
    
    for i in range(len(df_train)):
        for j in range(i, len(df_train)):
            train_dist[i, j] = distance[int(i * len(df_train) - (i*(i+1))/2 + j)]
            
#%%
# returns k most similar neighbors from the training set 
def getNeighbors(trainingSet, testInstance, k):
    min_dist = []
    for i in range(k):
#        print(testInstance, trainingSet[i])
        min_dist.append((i, trainingSet[i], levenshtein( testInstance, trainingSet[i])))    
    i_max = max(min_dist,key=operator.itemgetter(2))
    
    for j in range(k, len(trainingSet)):
        if(train_dist[i_max[0], j] <= 2 * i_max[2]):
            dist_c = levenshtein(testInstance, trainingSet[j])
            if(dist_c < i_max[2]):
                min_dist.append((j, trainingSet[j], dist_c))
                min_dist.remove(i_max)
                i_max = max(min_dist,key=operator.itemgetter(2))
    neighbors = []
    for x in range(k):
        neighbors.append(min_dist[x][1])
    print(neighbors)
    return neighbors

#    length = len(testInstance)-1
#    for x in range(len(trainingSet)):
#        dist = levenshtein(testInstance, trainingSet[x])
#        distances.append((trainingSet[x], dist))
#    distances.sort(key=operator.itemgetter(1))
#    neighbors = []
#    for x in range(k):
#        neighbors.append(distances[x][0])
#    return neighbors



#%%
# Give the label which is the most common in our neighbours
def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
    print(sortedVotes)
    return sortedVotes[0][0]

#%%
# return the accuracy in %
def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] is predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0

#%%
# Change the dataframe into a list
#list_train = df_train.values.tolist()
#list_test = df_test.values.tolist()

#%%
##Main function
#print(len(df_test))
#k = 3
## generate predictions
#predictions=[]
#for x in range(len(df_test)):
#    print(x)
#    neighbors = getNeighbors(df_train, df_test[x], k)
#    result = getResponse(neighbors)
#    predictions.append(result)
#	#print('> predicted=' + repr(result) + ', actual=' + repr(list_test[x][-1]))
#accuracy = getAccuracy(df_test, predictions)
#print('Accuracy: ' + repr(accuracy) + '% for k ='+repr(k))



for k in range(1,4):
    #Track run time
    start=time.time()
    
    # generate predictions
    predictions=[]
    for x in range(len(df_test)):
#        print(x)
        list_test_no_Nan = removeNan(df_test[x])
        neighbors = getNeighbors(df_train, list_test_no_Nan, k)
        result = getResponse(neighbors)
#        print(result)
        predictions.append(result)
        #End timer and show run time
        end=time.time()
        print(end-start)
        #print('> predicted=' + repr(result) + ', actual=' + repr(list_test_no_Nan[-1]))
    accuracy = getAccuracy(df_test, predictions)
    print('Accuracy: ' + repr(accuracy) + '% for k ='+repr(k))