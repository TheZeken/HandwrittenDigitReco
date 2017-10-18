# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 19:45:31 2017

First version of the knn

@author: jerem
"""
import math
import operator

#%%
#Import data and create histograms
# Database settings to downloads freeman codes
import pymysql
import pymysql.cursors

# Connect to the database.
conn = pymysql.connect(db='ml_db', user='root', passwd='', host='localhost')
sql_get_freeman = "SELECT `freeman`,`label` FROM `freeman_number`"

with conn.cursor() as cursor:
    cursor.execute(sql_get_freeman) #We execute our SQL request
    conn.commit()
    
    for row in cursor:
        print(row[0])
        
        

#%%
# Define the distance used in our knn

def euclideanDistance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)

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
	sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]

#%%
# return the accuracy in %
def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] is predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0


#%
#Main function


trainingSet=[]
testSet=[]
split = 0.67

# get data and split them between trainingset and testset

# generate predictions
predictions=[]
k = 3
for x in range(len(testSet)):
	neighbors = getNeighbors(trainingSet, testSet[x], k)
	result = getResponse(neighbors)
	predictions.append(result)
	print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
accuracy = getAccuracy(testSet, predictions)
print('Accuracy: ' + repr(accuracy) + '%')