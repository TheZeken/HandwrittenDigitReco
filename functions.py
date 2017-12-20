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
    sql_get_freeman = "SELECT `freeman`,`label` FROM `freeman_number`"
    
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
