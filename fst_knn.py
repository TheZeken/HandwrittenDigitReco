# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 19:45:31 2017

First version of the knn

@author: jerem
"""
import math
import operator
import numpy as np
import time
import pymysql
import pymysql.cursors
import pandas as pd
#%%
# Database settings to downloads freeman codes
# Connect to the database.
conn = pymysql.connect(db='ml_db', user='root', passwd='', host='localhost')
sql_get_freeman = "SELECT `freeman_prod`,`label` FROM `freeman_prod`"

sql_add_results = "INSERT INTO `knn_results` (`nb_train`, `nb_test`, `k_neighbours`, `accuracy`, `preprocess`, `distance`, `compute_time`,`nb_dataset`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
#%%
#Give the histograms given a str
#Usefull only if the euclidean distance is used
def hist(string):
    list_str = list(string)
    values_hist=[0,0,0,0,0,0,0,0]
    for i in list_str[0:-1]:
        values_hist[int(i)] +=1
    return values_hist
#%% Remove outliers regarding their freeman length
def removeOutliers(freeman):
    if len(freeman) > 90:
        return True
    elif len(freeman) < 10:
        return True
    else:
        return False
#%% 
#Remove Nan from a list
# Usefull for Edit Distance
def removeNan(chaine_):
    chaine1 = np.array([]).tolist()
    for i in range(len(chaine_)):
        if math.isnan(chaine_[i]):
            break
        else:
            chaine1.append(chaine_[i])
    return chaine1
#%%
with conn.cursor() as cursor:
    cursor.execute(sql_get_freeman) #We execute our SQL request
    conn.commit()
    
    df_train = pd.DataFrame()
    df_test = pd.DataFrame()
    
    cpt=0
    
#%%

# ------------------------------ Euclidean DISTANCE ---------------------------
#Comment this part if Euclidean distance is used   
def get_db_ecl():
    df_train = pd.DataFrame()
    #df_test = pd.DataFrame()
    #Histograms
    with conn.cursor() as cursor:
        cursor.execute(sql_get_freeman) #We execute our SQL request
        conn.commit()
        for row in cursor:
            values_hist=[]
            values_hist = hist(row[0])
            df2 = pd.DataFrame([[values_hist[0]],[values_hist[1]],[values_hist[2]],[values_hist[3]],[values_hist[4]],[values_hist[5]],[values_hist[6]],[values_hist[7]],[row[1]]])
            df_train = df_train.append(df2.T)
                
        list_train = df_train.values.tolist()
        return(list_train)
        #list_test = df_test.values.tolist()

#%%
# ----------------------------------- EDIT DISTANCE ---------------------------
#Comment this part if Edit distance is used
def get_db_edit():
    df_train = pd.DataFrame()
    #df_test = pd.DataFrame()
    #Histograms
    with conn.cursor() as cursor:
        cursor.execute(sql_get_freeman) #We execute our SQL request
        conn.commit()
        for row in cursor:        
            values =[int(i) for i in row[0]]
            values.append(row[1])
            df_train = df_train.append([pd.DataFrame(values).T])
        list_train = df_train.values.tolist()
        return(list_train)
#list_test = df_test.values.tolist()

#%%
# -----------------------------------Define the euclidean distance-------------
def euclideanDistance(instance1, instance2, length):
    distance = 0
    #print(length)
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)


#%%
#----------------------------------- Define the edit distance------------------
def levenshtein(chaine1, chaine2):
    cost=0
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
    return dist[len(chaine1),len(chaine2)]

#%% 
# ----------------------- Get Neighbors only for euclidean distance -----------
# returns k most similar neighbors from the training set 
"""
FOR PRODUCTION
"""
def getNeighbors_ecl(list_train,testInstance, k):
    distances = []
    testInstance = hist(testInstance)
    
    for x in range(len(list_train)):
        dist = euclideanDistance(testInstance, list_train[x], 1)
        distances.append((list_train[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors

#%%
# ----------------------- Get Neighbors only for Edit distance ----------------
# returns k most similar neighbors from the training set 
""" FOR PRODUCION"""
def getNeighbors_edit(list_train,testInstance, k,cross_val=False):
    distances = []
    #print(len(list_train))
    for x in range(len(list_train)):
        chaine2 = removeNan(list_train[x])
        if cross_val == False:
            testInstance = removeNan(testInstance)
            #print(chaine2[0:-1])
            dist = levenshtein(testInstance, chaine2[0:-1])
        elif cross_val == True:
            testInstance = removeNan(testInstance)
            dist = levenshtein(testInstance[0:-1], chaine2[0:-1])
        distances.append((chaine2, dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors
#%%
# ----------Give the label which is the most common in our neighbours----------
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
# -----------------------------------Return the accuracy in % -----------------
def getAccuracy(testSet, predictions):
    correct = 0
    print("length : ",len(testSet))
    for x in range(len(testSet)):
        testSet_no_Nan = removeNan(testSet[x])
        if testSet_no_Nan[-1] == predictions[x]:
            correct += 1
    return (correct/float(len(testSet))) * 100.0
