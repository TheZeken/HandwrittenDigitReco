# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 08:37:43 2017

@author: jerem
"""

import os
import struct
import numpy as np


##### definitions
path="C:\\Users\\edmon_000\\Desktop\\mldm year 2\\mldm project\\datasource\\"
size_x = 28
size_y = 28
#directions  =   [0,1,2,3,4,5,6,7] 
directions = 7
change_x    =   [-1,0, 1,
                  1,   1,
                  0,-1,-1]
change_y    =   [-1,-1,-1,
                 0,  1,
                 1, 1,0]

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
print(len(training_data))
label,pixels = training_data[1500]
print(label)
print(pixels.shape)

for x in range(0,28):
    for y in range (0,28):
        if pixels[x,y] > 100 :
            pixels[x,y] = 255
        else:
            pixels[x,y] = 0

print(pixels[10,12])
show(pixels)


for ii_x in range(0,size_x):
    for ii_y in range(0,size_y):
        if pixels[ii_x,ii_y] == 255:
            break

start_x = iix
start_y = iiy

curr_x = start_x
curr_y = start_y

visited[iix,iiy] = 1

"""
find first pixel - in a good image this will be the topmost and leftmost and this will be the starting point
check the 8 pixels around this pixel in a clockwise direction to determine the possible direction to move
this next pixel must be at the boundary (ie white space) and must be consecutive
create a grid of visited pixels
""""

# this is to test whether the next consecutive pixel is a contour or no
def iscontour(x,y):
    contour = False
    for (i, deltax) in enumerate(change_x):
            deltay = change_y[i]
            if pixels[x+deltax,y+deltay] == 0:
                contour = True
                break  # as long as there is atleast 1 white pixel, it is good
    return contour
        
def feasible (x,y):
        global pixels
        if pixels[x,y] == 0 and : 

            
visited = np.zeros (size_x,size_y)
for dirs in range(0,directions):
    potential_next_x = 




