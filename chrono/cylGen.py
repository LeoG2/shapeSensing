# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 15:03:08 2020

@author: lag37
"""

import math
import numpy as np
from edge_neighbourhood import edge_neighbourhood
from neighbours import neighboursNodes 

def cylGen(radius1, radius2,length,na,nl,neighbours ):
    
    """ 
    Genertae a 3D cylinder using nodes coordinates
    numbering starts in the circumference at point 0,0. once the 2pi is reahed
    the followinf number is on over the lenght. ]
    
    :param radius1:         radius 1 of the cylinder
    :param radius2:         radius 2 of the cylinder (circcle if r1=r2)
    :param length:          cylinder length
    :param na:              number of nodes per circumference
    :param nl:              number of nodes in the length
    :param neighbours:      mu,ber of neighbours(even numbers, 2,4,6,8)
    :return: (nodes, edges) nodes= nX3 matrix, n = total number of nodes
    edges = connectivity matrix, nx4, with n number of nodes and m number of 
    nodes connecting each n node. if -1, no edge exist
    """
    # Handle realistic values
    if na < 3: 
        raise ValueError(f"Number of nodes in the circumference must be >=3.")
    if nl < 2:
        raise ValueError(f"Number of nodes in the legth must be >=2.")
        
    nodes = []
    edges = []
    nidx = 0
    for i in range (nl):
        cl = length/(nl -1)*i   #current length
        
        for j in range(na):
            
            # make nodes list, 
            ca = j/na*2.*math.pi    #current angle in radians
            x = radius1 * math.cos(ca)
            y = radius2 * math.sin(ca)
            
            nodes.append([x,y,cl])
            
            # make edges
            
            #e = edge_neighbourhood(neighbours, nidx,j,i,na,nl)
            e = neighboursNodes(8, nidx, j, i, na, nl)
            edges.append(e)
            nidx += 1
            
    return np.array(nodes), np.array(edges)


