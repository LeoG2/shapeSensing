# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 14:17:02 2019

@author: Admin
"""

def eNeighbours(neighbours,nidx,a,l,na,nl):
    """
    identify the connecting nodes of nodes(idx) node
    
    :param neighbours:  number of neighbours to compute
    :param nidx:    node index
    :param a:   actual cross section node
    :param l:   actual cross section point  
    :param na:  number of segments on the cross section
    :param nl:  number of segment on the length 
    :return:    returns a connectivity matrix of the nodes connecting each node
        nxm, n= number of nodes, and m= number of neighbours
        1. read data form imported mesh (nodes coordinates) 
        2. get the number of nodes ans creates a ninference mesh
        3. identify the neighbours to compute
        4. create an array with the connectivity list for each N node. 
    """
    
# create an empty array to store connectivity list 

    e= [-1] * neighbours

    # link to the previous

    if a> 0:
        e[0]=nidx-1
    else:
        e[0]=nidx + na-1
    
    #link to the next
    
    if a<na-1:
        e[1]= nidx + 1
    else:
         e[1]=nidx-(na-1)
        
        # link to the left
    
    if l>0 and neighbours>2:
        e[2] = nidx - na
    
        #link to ang_prev left
    
        if neighbours > 4:
            if a>0:
                e[4]=nidx - na - l
            else:
                e[4]=nidx - 1
            
            #link to the next left
            
            if neighbours > 6:
                if a<na-1:
                    e[6] = nidx - na +1
                else:
                    e[6] = nidx + 1 -na -na;
            
#link to the right 

    if l<nl-1   and  neighbours>2:
        e[3] = nidx + na
    
    # link to the ang_next - right
    
        if neighbours > 4:
            if a<na-1:
                e[5] = nidx + na +1
            else:
                e[5] = nidx + 1
    
    #link to the prev right
    
        if neighbours > 6:
            if a > 0:
                e[7] = nidx + na - 1
            else:
                e[7] = nidx + na + na-1
    

    return e
        
        
        
        
    


    
    
    
    
    
    
    
    
    