# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 08:37:43 2017

@author: jerem
"""

import os
import struct
import numpy as np
import logging as lg

lg.basicConfig(level=lg.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


##### definitions
path="C:\\Users\\edmon_000\\Desktop\\mldm year 2\\mldm project\\datasource\\"
size_x = 28
size_y = 28
totalcells = size_x*size_y
#directions  =   [0,1,2,3,4,5,6,7] 
directions = 7


change_x    =   [0,  1,1,1,0,-1,-1, -1]
change_y    =   [-1,-1,0,1,1, 1, 0, -1]

"""
change_x    =   [-1,0, 1,
                  1,   1,
                  0,-1,-1]
change_y    =   [-1,-1,-1,
                 0,  1,
                 1, 1,0]
"""


start_x = 0
start_y = 0

freeman_chain = []


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
    


training_data = list(read(dataset="training", path=path))
lg.debug(len(training_data))
label,pixels = training_data[1501]
lg.debug(label)
lg.debug(pixels.shape)

for x in range(0,28):
    for y in range (0,28):
        if pixels[x,y] > 100 :
            pixels[x,y] = 255
        else:
            pixels[x,y] = 0

lg.debug(pixels[10,12])
show(pixels)


#find first starting pixel. inner loop is top down, outer loop is left to right
testpi = np.zeros ((size_x,size_y))
for ii_x in range(0,size_y):
    for ii_y in range(0,size_x):
        if pixels[ii_y,ii_x] == 255:
            #testpi[ii_y,ii_x] = i-200
            start_x = ii_x
            start_y = ii_y
            break
    else:
        continue
    break

curr_x = start_x
curr_y = start_y

lg.debug(curr_x)
lg.debug(curr_y)

visited = np.zeros ((size_y,size_x))
visited[ii_y,ii_x] = 1 #we have visited this pixel

"""
1. find first pixel - 
in a good image this will be the topmost and this will be the starting point

2.check the 8 pixels around this pixel in a clockwise direction to determine the possible direction to move
this next pixel in question:
   i. must be at the boundary (ie white space) 
   ii. and must be consecutive (connected to the previous pixel)
3.create a grid of visited pixels so that we don't back track accidentally
"""

# this is to test whether the next consecutive pixel is a contour or not
def iscontour(y,x):
    iscontour = False
    global change_y,change_x,pixels
    for (i, delta_x) in enumerate(change_x):
            delta_y = change_y[i]
            if pixels[y+delta_y,x+delta_x] == 0:
                iscontour = True
                break  # as long as there is at least 1 adjacent white pixel then this pixel is a contour
    return iscontour  

# this is to see if the next pixel to be moved into is feasible
def feasible (y,x):
        global pixels,visited
        if pixels[y,x] == 255 and iscontour(y,x) and visited[y,x] != 1:
            return True
        return False
    
cellsvisited = 0
stop = False

while (curr_y != start_y and curr_x != start_x or cellsvisited == 0) and cellsvisited <= 1200:
    cellsvisited = cellsvisited + 1
    for dirs in range(0,directions):
        #move into the first feasible pixel around a current pixel, while working in a clockwise direction
        if (feasible(curr_y+change_y[dirs],curr_x+change_x[dirs])):
            visited[curr_y,curr_x] = 1
            freeman_chain.append(dirs)
            curr_y = curr_y + change_y[dirs]
            curr_x = curr_x + change_x[dirs]
            testpi[curr_y,curr_x] = 30
            break
show(testpi)
  