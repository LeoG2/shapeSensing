# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 12:34:34 2019

@author: Admin
"""

import math
import numpy as np
from edge_neighbourhood import edge_neighbourhood


def cylGen(r1, r2, length, na, nl, neighbours):
    """
    Genertae a 3D cylindrical structure made of na nodes on cross section
    and nl nodes on the length. 
    
    Nodes numbering starts on pi=0 z=0, contineuo along pi, the pi @ z =1.
    
    :param r1     = radius 1 of cylinder ()
    :param r2     = radius 2 of cylinder (r1 = r2 if is a cicrcular cylinder,
                                     elliptical otherwise)
    :param length = cylinder length
    :param na     = number of divisions in pi
    :param nl     = number of divisions in length
    :param neighbours= number of connecting nodes to each node (2,4,6,8)
    :return: (nodes,edges) where 'nodes' is a matrix on Nx3, with N = total 
        number of nodes, 'edges' is teh connectivity matrix that contain the 
        indexes of the N nodes connecting to every N node. Startinf with
        [LN, RN, PN, NN]
    """

    # Handle unrealistic values
    if na<3:
        raise ValueError(f"Number of divisions on cross sesction must be >=3.")
    if nl<2:
        raise ValueError(f"Number of length divisions must be >= 2.")
        
# Nodes
    nodes=[];
    edges=[];
    nidx = 0;

    for i in range(nl):
        cl = length/ (nl-1)* i  # current length 
    
        for j in range(na):
            ca = j/na* 2. * math.pi   # current anlge in radians. 
            x  = r1 * math.cos(ca)
            y  = r2 * math.sin(ca)
            
            nodes.append([x,y,cl])
            
            e = eNeighbours(neighbours,nidx,j,i,na,nl)
            
            edges.append(e)
            
            nidx += 1

    return np.array(nodes), np.array(edges)
    
    run 3dScatter()
    
        