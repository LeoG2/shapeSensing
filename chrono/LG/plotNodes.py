# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 09:56:49 2019

@author: Admin

        node:   array containing nodes coordinates
        sty:    style to plot nodes


"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plotNodes(nodes,sty):
   
    
    x=nodes[:,0];
    y=nodes[:,1];
    z=nodes[:,2];
    
    fig = plt.figure();
    ax= fig.add_subplot(111,projection='3d')
    
    ax.scatter(x,y,z,c='b',marker='.')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    plt.show()
    
    