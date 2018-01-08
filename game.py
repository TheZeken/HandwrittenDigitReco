# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 16:20:01 2018

@author:  ishwar


Computer guesses number between 1...10
Input box for number -> user draw number
-> user prediction
-> number too high or low. Feedback
->Restart

"""

from random import  randint

#
def feedback (guessnumb,randnum):
    #choose lower number
    if guessnumb > randnum:
        return 3
    elif guessnumb == randnum:
        return 2
    
    #choose higher number
    else:
        return 1




def game():
    randnum = randint(1, 10)
    correct = False
    while correct is not True:
        
        #need to get this number from the interface
        usernumber = int(input("enter integer"))
        fdback = feedback(usernumber,randnum)
    
        #make the user choose higher number
        if fdback == 1:
            print("Choose higher number")
        elif fdback == 3:
            #make the user choose lower number
            print("choose lower number")
        else:
            correct = True

game()