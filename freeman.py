
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 08:37:43 2017

@author: jerem, ishwar
"""

import os
import struct
import numpy as np
import logging as lg


#%%
# Database settings to upload freeman codes
import pymysql
import pymysql.cursors

# Connect to the database.
#conn = pymysql.connect(db='ml_db', user='root', passwd='', host='localhost')
#
#sql_add_freeman = "INSERT INTO `freeman_number` (`freeman`, `label`) VALUES (%s,%s)"

#%%
# definitions
#path="C:\\Users\\jerem\\Desktop\\M2\\ML\\"

path = "../"

size_x = 28
size_y = 28
totalcells = size_x*size_y

directions = 8

""" surrounding pixels -
direction:[y,x] where xxx is the current pixel
we use 0:[-1,0] (up) as the current starting point

          
7:[-1,-1]    0:[-1,0]   1:[1,1]

6:[0,-1]     XXX        2:[0,1]

5:[-1,-1]   4:[1,0]     3:[1,1] 

"""


change_y    =   [-1,-1,0,1,1, 1, 0, -1]
change_x    =   [0,1,1,1,0,-1,-1, -1]


#%%
#Definition functions

#Read the MNIST dataset
def read(dataset = "training", path=path):
    """
    Python function for importing the MNIST data set.  It returns an iterator
    of 2-tuples with the first element being the label and the second element
    being a numpy.uint8 2D array of pixel data for the given image.
    """

    if dataset is "training":
        fname_img = os.path.join(path, 'train-images.idx3-ubyte')
        fname_lbl = os.path.join(path, 'train-labels.idx1-ubyte')
    elif dataset is "testing":
        fname_img = os.path.join(path, 't10k-images-idx3-ubyte')
        fname_lbl = os.path.join(path, 't10k-labels-idx1-ubyte')


    # Load everything in some numpy arrays
    with open(fname_lbl, 'rb') as flbl:
        magic, num = struct.unpack(">II", flbl.read(8))
        lbl = np.fromfile(flbl, dtype=np.int8)

    with open(fname_img, 'rb') as fimg:
        magic, num, rows, cols = struct.unpack(">IIII", fimg.read(16))
        img = np.fromfile(fimg, dtype=np.uint8).reshape(len(lbl), rows, cols)

    get_img = lambda idx: (lbl[idx], img[idx])

    # Create an iterator which returns each image in turn
    for i in range(len(lbl)):
        yield get_img(i)
        
# this is to test whether the next consecutive pixel is a contour or not, as we want to move into a border pixel
def iscontour(y,x):
    iscontour = False
    global change_y,change_x,pixels
    for (i, delta_x) in enumerate(change_x):
            delta_y = change_y[i]         
            # i am modding %2=0 because this selects only square adjacent directions and not corner directions. corners = merde*
            # Add the limit with x and y < 27 to avoid to go through the limit of the image
            if x==0 or x==size_x-1 or y==0 or y==size_y-1 or ( y+delta_y <size_y and x+delta_x < size_x and pixels[y+delta_y,x+delta_x] == 0 and i%2==0):
                iscontour = True
                break  # as long as there is at least 1 adjacent white pixel then this pixel is a contour
    return iscontour

# this is to see if the next pixel to be moved into is feasible
def feasible (y,x):
        global pixels,visited
        # if the next pixel (as computed by the dir) is black, contour and not visited
        if y!=-1 and x!=-1 and y!=size_y and x!=size_x and pixels[y,x] == 255 and iscontour(y,x) and visited[y,x] != 1:
            return True
        return False

def show(image):
    """
    Render a given numpy.uint8 2D array of pixel data.
    """
    from matplotlib import pyplot
    import matplotlib as mpl
    fig = pyplot.figure()
    ax = fig.add_subplot(1,1,1)
    imgplot = ax.imshow(image, cmap=mpl.cm.Greys)
    imgplot.set_interpolation('nearest')
    ax.xaxis.set_ticks_position('top')
    ax.yaxis.set_ticks_position('left')
    pyplot.show()

#%%
sample_image =  4663
### the image to test the freeman code

training_data = list(read(dataset="training", path=path))
lg.debug(len(training_data))

#for k in range(1001,5000):
label,pixels = training_data[sample_image]
lg.debug(label)
lg.debug(pixels.shape)
#=======

# on va convertir toute image en noir
for x_bw in range(0,size_x):
    for y_bw in range (0,size_y):
        if pixels[x_bw,y_bw] > 0 :
            pixels[x_bw,y_bw] = 255              
#
show(pixels)
#%%
#Find the starting point for the freeman function
start_x = 0
start_y = 0

for ii_y in range(0,size_y):
    for ii_x in range(0,size_x):
        if pixels[ii_y,ii_x] == 255:
            start_y = ii_y
            start_x = ii_x
            break
    else:
        continue
    break

curr_x = start_x
curr_y = start_y


#on utilise curr_x, curr_y ci-dessous dans la boucle pour qu'on puisse porcourir le contour
visited = np.zeros ((size_y,size_x)) # c'est pour se souvenir les pixels qu'on a deja parcouru
visited[curr_y,curr_x] = 1 #we have visited this pixel
    


#c'est pour le deboggage...on peux afficher cela pour bien voir le contour qu'il avait parcouru
freemancontour = np.zeros ((size_x,size_y))
freemancontour[curr_y,curr_x] = 255


"""
1. find first pixel to start

2.check the 8 pixels around this pixel in a clockwise direction to determine the possible direction to move
this next pixel in question:
   i. must be at the boundary (ie white space) 
   ii. and must be consecutive (connected to the previous pixel)
3.create a grid of visited pixels so that we don't back track accidentally
"""

freeman_chain = []
freeman_chain_str=""

disjoncteur = 1
#si on trouve qu'on a dépassé plusque 1 iteration sans bouger, le disjoncteur reste a 0, et la boucle s'arrete
while disjoncteur:
    disjoncteur = 0 
    for dirs in range(0,directions):
        #move into the first feasible pixel around a current pixel, while working in a clockwise direction ...dirs = 0 to 7
        if (feasible(curr_y+change_y[dirs],curr_x+change_x[dirs])):
            visited[curr_y,curr_x] = 1
            freeman_chain.append(dirs)
            freeman_chain_str +=str(dirs)
            curr_y = curr_y + change_y[dirs]
            curr_x = curr_x + change_x[dirs]
            disjoncteur = abs(change_y[dirs]) + abs(change_x[dirs]) 
            freemancontour[curr_y,curr_x] = 100
            #input("change_y " + str(change_y[dirs]) + " change x " + str(change_x[dirs]) + " dirs " + str(dirs) )
            break
show(freemancontour) ## affiche le plot du contour
print("freeman_chain = ",freeman_chain)
print(len(freeman_chain))
print("freeman_chain_str = " ,freeman_chain_str)
label_int = int(label)

#%%
#freeman_hist = np.zeros(directions)
#for i in freeman_chain:
#    freeman_hist[i] += 1
#print(freeman_hist)
#
#from matplotlib import pyplot                
#
#freeman_hist, bins, patches = pyplot.hist(freeman_chain)
#pyplot.show()
#print("freeman_hist = ", freeman_hist)
#%%
#Add to the database
#with conn.cursor() as cursor:
  #  cursor.execute(sql_add_freeman,(freeman_chain_str,label_int)) #We execute our SQL request
   # conn.commit()