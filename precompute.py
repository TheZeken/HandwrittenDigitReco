#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 15:38:26 2017

@author: mathieu
"""
import pymysql
import pymysql.cursors
import numpy as np
#from editDistance import levenshtein 
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
    return int(dist[len(chaine1),len(chaine2)])

def precomputeDistance(train_set, cursor):
    sql_add_distance = "INSERT INTO `precompute` (`dist`) VALUES (%s)"
#    precomputeDistance = {}
    for i in range(len(train_set)):
        for j in range(i, len(train_set)):
            precomputeDistance = levenshtein(train_set[i], train_set[j])
            print(i,j)
            cursor.execute(sql_add_distance, (precomputeDistance))
            
            
# Connect to the database.
conn = pymysql.connect(db='ml_db', user='root', passwd='23Octobre', host='localhost')
sql_get_freeman = "SELECT `freeman`,`label` FROM `freeman_number`"

cursor = conn.cursor()
# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS precompute")
print('ok')
# Create table as per requirement
sql = """CREATE TABLE precompute (
   DIST INT )"""

cursor.execute(sql)
print('ok')



#%%

cursor.execute(sql_get_freeman) #We execute our SQL request
conn.commit()

df_train = []
df_test = []

cpt=0

for row in cursor:
    
    if cpt < 600:
        cpt +=1
        values = row[0]
#            df2 = pd.DataFrame([[values_hist[0]],[values_hist[1]],[values_hist[2]],[values_hist[3]],[values_hist[4]],[values_hist[5]],[values_hist[6]],[values_hist[7]],[row[1]]])
        df_train.append(values)
#    else:
#        values = row[0]
##            df2 = pd.DataFrame([[values_hist[0]],[values_hist[1]],[values_hist[2]],[values_hist[3]],[values_hist[4]],[values_hist[5]],[values_hist[6]],[values_hist[7]],[row[1]]])
#        df_test.append(values)
                        
precomputeDistance(df_train, cursor)            
conn.commit()