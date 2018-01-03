# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 17:37:59 2017

@author: jerem
"""
import pymysql
import pymysql.cursors
#This file contain all the functions that are usefull

#%%
#Get average/max/min freeman length
# Connect to the database.
conn = pymysql.connect(db='ml_db', user='root', passwd='', host='localhost')

def get_max_min_avg():
    sql_get_freeman = "SELECT `freeman`,`label` FROM `freeman_prod`"
    
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
    print("Database reset Done")
    return True

def trunc_prod_db():
    SQL_reset_db="TRUNCATE TABLE freeman_prod"
    with conn.cursor() as cursor:
        cursor.execute(SQL_reset_db) #We execute our SQL request
        conn.commit()
    print("Database Truncated")