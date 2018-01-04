# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 17:37:59 2017

@author: jerem
"""
import pymysql
import pymysql.cursors
import numpy as np
import pandas as pd

from fst_knn import *

#This file contain all the functions that are usefull
conn = pymysql.connect(db='ml_db', user='root', passwd='', host='localhost')
#%%
#Get average/max/min freeman length
# Connect to the database.


def get_max_min_avg():
    sql_get_freeman = "SELECT `freeman_prod`,`label` FROM `freeman_prod`"
    
    with conn.cursor() as cursor:
        cursor.execute(sql_get_freeman) #We execute our SQL request
        conn.commit()
        
        cpt =0
        length = 0
        max_length = 0
        min_length = 100
        
        for row in cursor:
            #print(len(row[0]))
            length += len(row[0])
            cpt+=1
            if len(row[0]) > max_length:
                max_length = len(row[0])
            elif len(row[0]) < min_length:
                min_length = len(row[0])
        
        print(cpt)
        print("Max length = ", max_length)
        print("Min Length = ", min_length)
        print("Average length = ",length/cpt)
        return max_length,min_length,(length/cpt)


def reset_prod_db():
    SQL_reset_db="TRUNCATE TABLE freeman_prod"
    SQL_get_freeman = "SELECT * FROM `freeman_number` WHERE id_freeman <= 100"
    SQL_insert_prod = "INSERT INTO `freeman_prod`(`id_freeman_prod`, `freeman_prod`, `label`) VALUES (%s,%s,%s)"
    
    with conn.cursor() as cursor:
        cursor.execute(SQL_reset_db) #We execute our SQL request
        cursor.execute(SQL_get_freeman) #We execute our SQL request
        conn.commit()
        for row in cursor:
            with conn.cursor() as cursor2:
                cursor2.execute(SQL_insert_prod,(row[0],row[1],row[2])) #We execute our SQL request
                conn.commit()
    print("Database Mnist reset Done")
    global train_list_edit,train_list_ecl
    train_list_edit = get_db_edit()
    train_list_ecl = get_db_ecl()
    return True

def reset_our_prod_db():
    SQL_reset_db="TRUNCATE TABLE freeman_prod"
    SQL_get_freeman = "SELECT * FROM `freeman_our`"
    SQL_insert_prod = "INSERT INTO `freeman_prod`(`id_freeman_prod`, `freeman_prod`, `label`) VALUES (%s,%s,%s)"
    
    with conn.cursor() as cursor:
        cursor.execute(SQL_reset_db) #We execute our SQL request
        cursor.execute(SQL_get_freeman) #We execute our SQL request
        conn.commit()
        for row in cursor:
            with conn.cursor() as cursor2:
                cursor2.execute(SQL_insert_prod,(row[0],row[1],row[2])) #We execute our SQL request
                conn.commit()
    print("Database our reset Done")
    global train_list_edit,train_list_ecl
    train_list_edit = get_db_edit()
    train_list_ecl = get_db_ecl()
    return True

def trunc_prod_db():
    SQL_reset_db="TRUNCATE TABLE freeman_prod"
    with conn.cursor() as cursor:
        cursor.execute(SQL_reset_db) #We execute our SQL request
        conn.commit()
    global train_list_edit,train_list_ecl
    train_list_edit = get_db_edit()
    train_list_ecl = get_db_ecl()
    return True
    print("Database Truncated")

def get_cross_val_score(e1):
    if e1.get() != "":
        k = int(e1.get())
    else:
        k=5
    SQL_count = "SELECT COUNT(*) FROM `freeman_prod`"
    with conn.cursor() as cursor:
        cursor.execute(SQL_count) #We execute our SQL request
        conn.commit()
        for row in cursor:
            nb_inst = row[0]
            
    nb_inst_mat = int(nb_inst/k)
    
    accuracy = np.zeros(k)
    accuracy_global = 0
    SQL_get_freeman = "SELECT * FROM `freeman_prod`"

    
    for i in range(1,k+1):
        df_train = pd.DataFrame()
        df_test = pd.DataFrame()
        cpt = 0
        with conn.cursor() as cursor:
            cursor.execute(SQL_get_freeman) #We execute our SQL request
            conn.commit()
            for row in cursor:
                if cpt < i*nb_inst_mat and cpt >= i*nb_inst_mat-nb_inst_mat:
                    cpt+=1
                    values =[int(i) for i in row[1]]
                    values.append(row[2])
                    df_test = df_test.append([pd.DataFrame(values).T])
                else:
                    cpt+=1
                    values =[int(i) for i in row[1]]
                    values.append(row[2])
                    df_train = df_train.append([pd.DataFrame(values).T])
            list_train = df_train.values.tolist()
            list_test = df_test.values.tolist()
            
            predictions = np.zeros(len(list_test))
            for j in range(0,len(list_test)):
                neighbours = getNeighbors_edit(list_train,list_test[j], 3,True)
                predictions[j]= getResponse(neighbours)
                    
            accuracy[i-1] = getAccuracy(list_test,predictions)
            print(accuracy[i-1])
    for h in range(0,k):
        accuracy_global += accuracy[h]
    print(accuracy_global/k)
    return accuracy_global/k
        
def process_db():
    list_train = get_db_edit()
    
    mat = np.zeros((len(list_train),len(list_train)))
    mean_global = 0
    max_global = 0
    min_global = 1000
    mean_mat = np.zeros(len(list_train))
    cpt = 0
    
    for i in range(0,len(list_train)):
        mean = 0
        max_ = 0
        min_ = 1000
        chaine1 = removeNan(list_train[i])
        for j in range(0,len(list_train)):
            chaine2 = removeNan(list_train[j])
            if i != j and chaine1[-1] == chaine2[-1]:
                mat[i][j] = levenshtein(chaine1[0:-1],chaine2[0:-1]) 
                if mat[i][j] > max_:
                    max_ = mat[i][j]
                if mat[i][j] < min_:
                    min_ = mat[i][j]
                mean += mat[i][j]
        #print("Done for i = ",i,"With label =",chaine1[-1])
       # print("For i =",i," We have the following values:")
        #print("Compared to ", cpt, "other")
        #print("Max =", max_)
        #print("Min = ", min_)
        #print("Mean =" , mean/cpt)
        mean_mat[i] = mean/cpt
        
    delete_SQL = "DELETE FROM `freeman_prod` WHERE `id_freeman_prod` = %s"
    
    label_done = np.zeros(10)
    for i in range(0,len(list_train)):
        chaine1 = removeNan(list_train[i])
        for j in range(0,len(list_train)):
            chaine2 = removeNan(list_train[j])
            if mat[i][j] != 0:
                if mat[i][j] < 10 and chaine1[-1] == chaine2[-1]:
                     with conn.cursor() as cursor:
                        cursor.execute(delete_SQL,(j+1)) #We execute our SQL request
                        conn.commit()
                        cpt+=1
                        #print("Number with id_freeman_prod =",j+1,"has been deleted")
        label_done[int(chaine1[-1])] = 1
                
        
    return True, cpt   
    print("DONE")

    
    
    
    
    
    
    
    
    
    
    
    
    
    