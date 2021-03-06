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
sql_get_freeman = "SELECT `freeman`,`label` FROM `freeman_number`"

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
            if int(chaine1[i-1]) == int(chaine2[j-1]):
                cost = 0
            elif (int(chaine2[j-1]) - int(chaine1[i-1])) %8 == 1:
                cost = 0.5
            elif (int(chaine2[j-1]) - int(chaine1[i-1])) %8 == 2:
                cost = 1
            elif (int(chaine2[j-1]) - int(chaine1[i-1])) %8 == 3:
                cost = 1.5
            elif (int(chaine2[j-1]) - int(chaine1[i-1])) %8 == 4:
                cost = 2
            elif (int(chaine2[j-1]) - int(chaine1[i-1])) %8 == 5:
                cost = 1.5
            elif (int(chaine2[j-1]) - int(chaine1[i-1])) %8 == 6:
                cost = 1
            elif (int(chaine2[j-1]) - int(chaine1[i-1])) %8 == 7:
                cost = 0.5
            dist[i,j] = min(dist[i-1, j]+1, dist[i, j-1]+1, dist[i-1, j-1]+cost)
    return dist[len(chaine1),len(chaine2)]
#%%
#----------------------------------- Define the edit distance With triangle inequality------------------
def levenshtein_ineq(string1, string2):
#    print(string1)
    chaine1 = list(string1)
    chaine2 = list(string2)
    chaine1 = chaine1[0:-1]
    chaine2 = chaine2[0:-1]
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
    return dist[len(chaine1),len(chaine2)]


#%% 
# ----------------------- Get Neighbors only for euclidean distance -----------
# returns k most similar neighbors from the training set 
"""
FOR PRODUCTION
"""
def getNeighbors_ecl(list_train,testInstance, k,cross_val=False,db="mnist"):
    if db == "mnist":
        k = 5
    else:
        k=1
        
    distances = []
    testInstance = removeNan(testInstance)
    testInstance = hist(testInstance)
    
    for x in range(len(list_train)):
        if cross_val == True:
            train_hist = removeNan(list_train[x])
            train_hist = hist(train_hist)
        else:
            train_hist = list_train[x]
        dist = euclideanDistance(testInstance, train_hist, 8)
        distances.append((train_hist, dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors

#%%
# ----------------------- Get Neighbors only for Edit distance ----------------
# returns k most similar neighbors from the training set 
""" FOR PRODUCION"""
def getNeighbors_edit(list_train,testInstance, k,cross_val=False,db="mnist"):
    distances = []
    if db == "mnist":
        k = 5
    else:
        k=1
    dist = []
    #print(len(list_train))
    for x in range(len(list_train)):
        if db != "seq":
            chaine2 = removeNan(list_train[x])
        else:
            chaine2 = list_train[x]
        if cross_val == False:
            testInstance = removeNan(testInstance)
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
# ----------------------- Get Neighbors only for Edit distance with triangle inequality ----------------
# returns k most similar neighbors from the training set 
def getNeighbors_edit_ineq(trainingSet, testInstance, k):
    sql_get_distance = "SELECT `dist` FROM `precompute`"
    with conn.cursor() as cursor:
        cursor.execute(sql_get_distance) #We execute our SQL request
        conn.commit()
        
        train_dist = {}    
        distance = []
        for row in cursor:
            distance.append(row)
        
        for i in range(len(trainingSet)):
            for j in range(i, len(trainingSet)):
                train_dist[i, j] = distance[int(i * len(trainingSet) - (i*(i+1))/2 + j)]

    min_dist = []
    for i in range(k):
        chaine2 = removeNan(trainingSet[i])
        min_dist.append((i, chaine2, levenshtein_ineq( testInstance, chaine2)))    
    i_max = max(min_dist,key=operator.itemgetter(2))
    indiceTraining = list(range(k, len(trainingSet)))
    
    for j in indiceTraining:
        chaine2_j = removeNan(trainingSet[j])
        dist_c = levenshtein_ineq(testInstance, chaine2_j)
        if(dist_c < i_max[2]):
            min_dist.append((j, chaine2_j, dist_c))
            min_dist.remove(i_max)
            i_max = max(min_dist,key=operator.itemgetter(2))
        else:
            i = j+1
            while i != len(trainingSet):
                if(train_dist[j,i] < dist_c - i_max[2]):
                    if i in indiceTraining:
                        indiceTraining.remove(i)
                elif(train_dist[j,i] > dist_c + i_max[2]):
                    if i in indiceTraining:
                        indiceTraining.remove(i)
                i +=1 
                while not(i in indiceTraining) & i != len(trainingSet):
                    i+=1
    neighbors = []
    for x in range(k):
#        print(min_dist[x][0])
        neighbors.append(min_dist[x][1])
#    print(neighbors)
    
#    print(testInstance)
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
