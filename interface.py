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
from functions import *

from skimage.transform import resize

from tkinter import *
from tkinter import messagebox
import skimage.io as ski_io

fen = Tk()
fen.title("Digit Recognition Tool")
# frame 1
Frame1 = Frame(fen, borderwidth=2, relief=GROOVE)
Frame1.pack(side=LEFT, padx=30, pady=30)

# frame Frame1_2
Frame1_2 = Frame(Frame1, borderwidth=2, relief=GROOVE)
Frame1_2.pack(side=RIGHT, padx=10, pady=10)

# frame 2
Frame2 = Frame(fen, borderwidth=2, relief=GROOVE)
Frame2.pack(side=LEFT, padx=4, pady=10)

# frame 2-1
Frame2_1 = Frame(Frame2, borderwidth=2, relief=GROOVE)
Frame2_1.pack(side=BOTTOM, padx=4, pady=10)

# frame 1-1
Frame1_1= Frame(Frame1, borderwidth=0, relief=GROOVE)
Frame1_1.pack(side=BOTTOM, padx=2, pady=2)

img = np.zeros((WIDTH_CANVAS,HEIGHT_CANVAS))

train_list_edit = get_db_edit()
train_list_ecl = get_db_ecl()

db = "mnist"

#%%
# Prediction Part
def predict_ecl(freeman_chain_str,db):
    neighbors = getNeighbors_ecl(train_list_ecl,freeman_chain_str, 3,db)
    result = getResponse(neighbors)
    return result

def predict_edit(freeman_chain_str,db):
    neighbors = getNeighbors_edit(train_list_edit,freeman_chain_str, 3,False,db)
    result = getResponse(neighbors)
    return result
    
def predict_can(fen,db):
    img_ = np.zeros((28,28))
    global img,value
    for i in range(0,WIDTH_CANVAS-3):
        for j in range(0,HEIGHT_CANVAS-3):
            if img_[int(i/4),int(j/4)] == 0 and img[i,j] == 255 and int(i/4) < 27 and int(j/4) < 27:
                img_[int(i/4),int(j/4)] = 255
                img_[int(i/4)+1,int(j/4)+1] = 255
                img_[int(i/4)-1,int(j/4)-1] = 255
             
    scipy.misc.imsave('outfile.jpg', img_)  
    freeman_chain,freeman_chain_str = get_freeman(img_)

    if str(value.get()) == "both":
        label_pred.config(text = "Prediction Edit : " + str(predict_edit(freeman_chain,db)) + "\n Prediction Euclidean : "+ str(predict_ecl(freeman_chain,db)))
    elif str(value.get()) == "ecl":
        label_pred.config(text = " Prediction Euclidean : "+ str(predict_ecl(freeman_chain,db)))
    elif str(value.get()) == "edit":
        label_pred.config(text = "Prediction Edit : " + str(predict_edit(freeman_chain,db)))

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

predict_btn = Button(Frame1, text='Predict', borderwidth=2, command=lambda: predict_can(fen,db)).pack(side=LEFT)
clear_btn = Button(Frame1, text='Clear Canvas', borderwidth=2,command= clear_canvas).pack(side=RIGHT)

label_pred = Label(Frame1_1)
label_pred.pack()
#%% Popup for information
def reset_prod_db_tk():
    global db
    db= "mnist"
    if reset_prod_db():
        messagebox.showinfo("Information", "The database has been reseted to : Mnist (100)")
    else:
        messagebox.showinfo("Information", "Something went wrong during the reset, please try again.")

def trunc_prod_db_tk():
    global db
    db= "other"
    if trunc_prod_db():
        messagebox.showinfo("Information", "The database is now empty")
    else:
        messagebox.showinfo("Information", "Something went wrong, please try again.")

def reset_our_prod_db_tk():
    global db
    db= "our"
    if reset_our_prod_db():
        messagebox.showinfo("Information", "The database has been reseted to : Ours ")
    else:
        messagebox.showinfo("Information", "Something went wrong during the reset, please try again.")
        
def process_db_tk():
    global db
    db= "other"
    bina, cpt = process_db()
    if bina:
        messagebox.showinfo("Information", str(cpt)+" Irrevelants training example removed")
    else:
        messagebox.showinfo("Information", "Something went wrong, please try again.")

#%%
#Data Base Module
clear_db = Button(Frame2, text='Get Mnist / Reset DB', borderwidth=2,command= reset_prod_db_tk).pack(side=LEFT)
trunc_db = Button(Frame2, text='Truncate Database', borderwidth=2,command= trunc_prod_db_tk).pack(side=LEFT)
our_db = Button(Frame2, text='Get Ours / Reset DB', borderwidth=2,command= reset_our_prod_db_tk).pack(side=LEFT)
process_db_btn = Button(Frame2, text='Clean DB', borderwidth=2,command= process_db_tk).pack(side=LEFT)

v_e1 = StringVar()
cross_val_score = Button(Frame2_1, text='Cross Validation score Edit', borderwidth=2,command= lambda: get_cross_val_score(v_e1,db)).pack(side=BOTTOM)
cross_val_score = Button(Frame2_1, text='Cross Validation score Euclidean', borderwidth=2,command= lambda: get_cross_val_score_ecl(v_e1,db)).pack(side=BOTTOM)
e1 = Entry(Frame2_1,textvariable = v_e1).pack(side=BOTTOM)


def add_db(val):
    # Connect to the database.
    conn = pymysql.connect(db='ml_db', user='root', passwd='', host='localhost')
    SQL_add_canvas = "INSERT INTO `freeman_prod`(`freeman_prod`, `label`) VALUES (%s,%s)"
        
    img_ = np.zeros((28,28))
    global img,value
    for i in range(0,WIDTH_CANVAS-3):
        for j in range(0,HEIGHT_CANVAS-3):
            if img_[int(i/4),int(j/4)] == 0 and img[i,j] == 255 and int(i/4) < 27 and int(j/4) < 27:
                img_[int(i/4),int(j/4)] = 255
                img_[int(i/4)+1,int(j/4)+1] = 255
                img_[int(i/4)-1,int(j/4)-1] = 255
             
    scipy.misc.imsave('outfile.jpg', img_)  
    freeman_chain,freeman_chain_str = get_freeman(img_)
    
    with conn.cursor() as cursor:
        cursor.execute(SQL_add_canvas,(freeman_chain_str,val)) #We execute our SQL request
        conn.commit()
    global train_list_edit,train_list_ecl
    train_list_edit = get_db_edit()
    train_list_ecl = get_db_ecl()
    
    


#%%
buttons=np.zeros(10)
for ligne in range(2):
    for colonne in range(5):
        if ligne == 0:
            buttons[ligne+colonne] = Button(Frame1_2, text='%s' % (ligne+colonne), borderwidth=2, command=lambda ligne=ligne, colonne=colonne: add_db(ligne+colonne)).grid(row=ligne, column=colonne)
        else:
            buttons[5+colonne] = Button(Frame1_2, text='%s' % (5+colonne), borderwidth=2,command=lambda colonne=colonne: add_db(5+colonne)).grid(row=ligne, column=colonne)
#%%

fen.mainloop()