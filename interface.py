# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 15:03:28 2017

@author: jerem
"""

WIDTH_CANVAS = 112
HEIGHT_CANVAS = 112

import numpy as np

import scipy.misc

from fst_knn import *
from freeman import *

from skimage.transform import resize

from tkinter import *
import skimage.io as ski_io

fen = Tk()
# frame 1
Frame1 = Frame(fen, borderwidth=2, relief=GROOVE)
Frame1.pack(side=LEFT, padx=30, pady=30)

# frame 2
Frame2 = Frame(fen, borderwidth=2, relief=GROOVE)
Frame2.pack(side=LEFT, padx=10, pady=10)

# frame 3
Frame1_1= Frame(Frame1, borderwidth=0, relief=GROOVE)
Frame1_1.pack(side=BOTTOM, padx=2, pady=2)

img = np.zeros((WIDTH_CANVAS,HEIGHT_CANVAS))

train_list_edit = get_db_edit()
train_list_ecl = get_db_ecl()

#%%
# Prediction Part
def predict_ecl(freeman_chain_str):
    neighbors = getNeighbors_ecl(train_list_ecl,freeman_chain_str, k=3)
    result = getResponse(neighbors)
    return result

def predict_edit(freeman_chain_str):
    neighbors = getNeighbors_edit(train_list_edit,freeman_chain_str, k=3)
    result = getResponse(neighbors)
    return result
    
def predict_can(fen):
    img_ = np.zeros((28,28))
    global img,value
    for i in range(0,WIDTH_CANVAS-3):
        for j in range(0,HEIGHT_CANVAS-3):
            if img_[int(i/4),int(j/4)] == 0 and img[i,j] == 255 and int(i/4) < 27 and int(j/4) < 27:
                img_[int(i/4),int(j/4)] = 255
                img_[int(i/4)+1,int(j/4)+1] = 255
                img_[int(i/4)-1,int(j/4)-1] = 255
             
    scipy.misc.imsave('outfile.jpg', img_)  
    freeman_chain_str = get_freeman(img_)

    if str(value.get()) == "both":
        label_pred.config(text = "Prediction Edit : " + str(predict_edit(freeman_chain_str)) + "\n Prediction Euclidean : "+ str(predict_ecl(freeman_chain_str)))
    #print("prediction Edit : ",predict_edit(freeman_chain_str))    
    #print("prediction Euclidean : ",predict_ecl(freeman_chain_str))
    
    
    
    


#%%

#Draw Module
def draw (event): #Un argument est envoyé automatiquement à la fonction suite au can.bind(...), c'est
    global WIDTH_CANVAS,HEIGHT_CANVAS
    x,y = event.x,event.y #une instance d'une classe qui fournit les coordonnées du clic dans le canvas
    #par le biais de ses attributs x et y (le nom event est donné à l'argument
                                           #conventionnellement
    can.create_oval(x-8,y-8,x+8,y+8, fill='black') #on crée un cercle de centre les coordonnées du clic dans notre Canvas "can"
    if y < WIDTH_CANVAS and x < HEIGHT_CANVAS:
        img[y,x] = 255
        img[y+1,x+1] = 255
        img[y-1,x-1] = 255

def desactivate(envent):
    can.unbind("<Motion>")
    
def activate(event):
    can.bind("<Motion>", draw)
    
def clear_canvas():
    global WIDTH_CANVAS,HEIGHT_CANVAS,img
    can.delete("all")
    img = np.zeros((WIDTH_CANVAS,HEIGHT_CANVAS))

can = Canvas(Frame1, width =WIDTH_CANVAS, height =HEIGHT_CANVAS, bg="white")
can.bind("<Button-1>", activate) #on lie le clic gauche à la fonction "rond"
can.bind("<ButtonRelease-1>", desactivate) #on lie le clic gauche à la fonction "rond"
can.pack()

# Select wanted distance to predict
value = StringVar() #Its value corrspoend to the selected distance
value.set("both")
ecl_dist = Radiobutton(Frame1, text="Euclidean", variable=value, value="ecl")
edt_dist = Radiobutton(Frame1, text="Edit", variable=value, value="edit")
both_dist = Radiobutton(Frame1, text="Both", variable=value, value="both")
ecl_dist.pack()
edt_dist.pack()
both_dist.pack()

predict_btn = Button(Frame1, text='Predict', borderwidth=2, command=lambda: predict_can(fen)).pack(side=LEFT)
clear_btn = Button(Frame1, text='Clear Canvas', borderwidth=2,command= clear_canvas).pack(side=RIGHT)

label_pred = Label(Frame1_1)
label_pred.pack()

#%%
buttons=np.zeros(10)
for ligne in range(2):
    for colonne in range(5):
        if ligne == 0:
            buttons[ligne+colonne] = Button(Frame2, text='%s' % (ligne+colonne), borderwidth=2).grid(row=ligne, column=colonne)
        else:
            buttons[5+colonne] = Button(Frame2, text='%s' % (5+colonne), borderwidth=2).grid(row=ligne, column=colonne)
#%%

fen.mainloop()