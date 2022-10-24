# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 23:20:14 2021

@author: 2stic
"""

import PIL
import numpy as np
import matplotlib.pyplot as plt
import math
import colour
import random

    
#%%
def distance(pointA,pointB):
    distsq = 0
    for i in range(3):
        distsq += (pointA[i] - pointB[i])**2
    dist = math.sqrt(distsq)
    return dist

#%%

def isNeighbour(pointA,pointB,limit):
    return distance(pointA,pointB) < limit

def makeNeighbourhood(centre,pointlist,limit):
    neighbourhood = []
    for i in pointlist:
        if isNeighbour(centre,i,limit):
            neighbourhood.append(i)
    return neighbourhood
    

#%%
def listminus(list1,list2):
    out = []
    for i in range(len(list1)):
        out.append(list1[i]-list2[i])
    return out

def listadd(list1,list2):
    out = []
    for i in range(len(list1)):
          out.append(list1[i]+list2[i])
    return out
    

#%%

im = PIL.Image.open("gyarados.png").convert('RGB')

imArray = np.array(im)

hue, sat, value = imArray.T

data = im.getcolors()

imColours = [i[1] for i in data]

imFreq = [i[0] for i in data]

imColoursCopy = imColours.copy()

neighbourhoods = []

while len(imColoursCopy) > 0:
    n = makeNeighbourhood(imColoursCopy[0],imColoursCopy,100)
    neighbourhoods.append(n)
    for i in n:
        try:
            imColoursCopy.remove(i)
        except ValueError:
            print()
 
#%%
dat = im.getpalette()

rgbVals = []

while len(dat) > 0:
    rgbVals.append(dat[:3])
    for i in range(3):
        dat.pop(0)
        


rgbVals = rgbVals[:16]

rgbColour = []

for i in rgbVals:
    c = colour.Color(rgb=(i[0]/255,i[1]/255,i[2]/255))
    rgbColour.append(c)

rgbString = []

for i in rgbVals:
    rgbString.append("rgb({},{},{})".format(i[0],i[1],i[2]))
#%%
for i in range(len(rgbString)):
    new = PIL.Image.new("RGB",(16,16),color=rgbString[i])
    name = "Col{}.png".format(i)
    new.save(name, "png")
    
#%%
nHSL = []

for i in rgbColour:
    neighbourhood = []
    for j in rgbColour:
        if isNeighbour(i.hsl,j.hsl,0.35):
            neighbourhood.append(j)
    nHSL.append(neighbourhood)
    
#%%
test = []
for i in nHSL:
    if i not in test:
        test.append(i)
#%%
for i in test:
    out = "Neighbourhood of {} consists of: ".format(nHSL.index(i))
    for j in i:
        out += str(rgbColour.index(j)) + ","
    print(out)
   #%%
neighbourVectors = []
for neighbourhood in neighbourhoods:
    n = []
    for point in neighbourhood:
         n.append(tuple(listminus(neighbourhood[0],point)))
    neighbourVectors.append(n)
    
#%%
for k in range(100):
    imArray = np.array(im)
    hue, sat, value = imArray.T

    adjustedVector = []
    for neighbourhood in neighbourVectors:
        random_colour = [random.randint(0,255) for i in range(3)]
        adjustedVector.append([listadd(i,random_colour) for i in neighbourhood])
            
    for i in range(len(neighbourhoods)):
        for j in range(len(neighbourhoods[i])):
            area = (hue == neighbourhoods[i][j][0]) & (sat == neighbourhoods[i][j][1]) & (value == neighbourhoods[i][j][2])
            imArray[...][area.T] = tuple(adjustedVector[i][j])

    PIL.Image.fromarray(imArray).save("random {}.png".format(str(k)),"png")
    