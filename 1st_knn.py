# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 19:45:31 2017

First version of the knn

@author: jerem
"""
import math
import operator
import numpy as np

#%%
#Import data and create histograms
# Database settings to downloads freeman codes
import pymysql
import pymysql.cursors
import pandas as pd

# Connect to the database.
conn = pymysql.connect(db='ml_db', user='root', passwd='', host='localhost')
sql_get_freeman = "SELECT `freeman`,`label` FROM `freeman_number`"
#%%
#Give the histograms given a str
def hist(string):
    list_str = list(string)
    values_hist=[0,0,0,0,0,0,0,0]
    for i in list_str:
        values_hist[int(i)] +=1
    return values_hist

#%%
with conn.cursor() as cursor:
    cursor.execute(sql_get_freeman) #We execute our SQL request
    conn.commit()
    
    df_train = pd.DataFrame()
    df_test = pd.DataFrame()
    
    cpt=0
    
    for row in cursor:
        values_hist=[]
        
        if cpt < 6000:
            cpt +=1
            values_hist = hist(row[0])
            df2 = pd.DataFrame([[values_hist[0]],[values_hist[1]],[values_hist[2]],[values_hist[3]],[values_hist[4]],[values_hist[5]],[values_hist[6]],[values_hist[7]],[row[1]]])
            df_train = df_train.append(df2.T)
        else:
            values_hist = hist(row[0])
            df2 = pd.DataFrame([[values_hist[0]],[values_hist[1]],[values_hist[2]],[values_hist[3]],[values_hist[4]],[values_hist[5]],[values_hist[6]],[values_hist[7]],[row[1]]])
            df_test = df_test.append(df2.T)
                
    
#%%
# Define the euclidean distance
def euclideanDistance(instance1, instance2, length):
    distance = 0
    #print(length)
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)


#%%
# Define the edit distance
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


#%%
# returns k most similar neighbors from the training set 
def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance)-1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors

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
list_train = df_train.values.tolist()
list_test = df_test.values.tolist()

#%%
#Main function

k = 4
# generate predictions
predictions=[]
for x in range(len(list_test)):
	neighbors = getNeighbors(list_train, list_test[x], k)
	result = getResponse(neighbors)
	predictions.append(result)
	#print('> predicted=' + repr(result) + ', actual=' + repr(list_test[x][-1]))
accuracy = getAccuracy(list_test, predictions)
print('Accuracy: ' + repr(accuracy) + '% for k ='+repr(k))