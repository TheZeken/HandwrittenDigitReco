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
    sql_get_freeman = "SELECT `sequence_freeman`,`val_sequence` FROM `sequences`"
    
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


        
def process_db():
    list_train = get_db_edit()
    
    mat = np.zeros((len(list_train),len(list_train)))
    mean_mat = np.zeros(len(list_train))

    for i in range(0,len(list_train)):
        cpt = 0
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
                cpt+=1
        mean_mat[i] = mean/cpt
        print(mean_mat[i])
        
    delete_SQL = "DELETE FROM `freeman_prod` WHERE `id_freeman_prod` = %s"
    
    cpt = 0
    
    label_done = np.zeros(10)
    for i in range(0,len(list_train)):
        chaine1 = removeNan(list_train[i])
        if label_done[int(chaine1[-1])] == 0:
            for j in range(0,len(list_train)):
                chaine2 = removeNan(list_train[j])
                if mat[i][j] != 0:
                    if mat[i][j] < mean_mat[i] and chaine1[-1] == chaine2[-1]:
                         with conn.cursor() as cursor:
                            cursor.execute(delete_SQL,(j+1)) #We execute our SQL request
                            conn.commit()
                            cpt+=1
                            #print("Number with id_freeman_prod =",j+1,"has been deleted")
            label_done[int(chaine1[-1])] = 1
            
        
    return True, cpt   
    

    
    
    
    
    
    
    
    