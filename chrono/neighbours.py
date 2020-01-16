# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 10:46:24 2020

@author: lag37
"""
def neighboursNodes(neighbours,nidx,a,l,na,nl):
    """
    

    Parameters
    ----------
    neighbours : TYPE integer(2,4,6,8)
        DESCRIPTION.number of neighbours to be computed per node
    nidx : TYPE     integer, 
        DESCRIPTION. node index to compute neighbours nodes
    a : TYPE    integer
        DESCRIPTION.    Actual node 
    l : TYPE    integer
        DESCRIPTION. actual length segment
    na : TYPE   integer
        DESCRIPTION. Number of nodes in cross section
    nl : TYPE   integer
        DESCRIPTION. Number of segments in the length of cylinder. 

    Returns: a conectivity array of n x m. n= 1= nidx, m=neighbours.  
    -------
    None.

    #      #       #
      \    |     /
        6   0   5
          \ | /
    #-- 2 --#-- 3 --#
          / | \
        4   1   7
      /     |     \
    #       #       #
          
          connectiity matrix 
    """

    e = [-1] * neighbours
     
    #link to previus node
    if a>0:
        e[0] = nidx-1
    else:
        e[0] = nidx + (na-1)
         
     # link to next node
    if a < na-1:
            e[1] = nidx+1
    else:
            e[1] = nidx - (na-1)
            
                
     
    # link to the left
    if l> 0 and neighbours > 2:
        e[2]= nidx-na
        # link to ang_prev -left
        if neighbours > 4:
            if a > 0:
                e[4] = nidx -na-1
            else:
                e[4] = nidx -1
       # link to the ang_next - left
            if  neighbours > 6:
                if a < na - 1:
                    e[6] = nidx - na + 1
                else: 
                    e[6] = nidx + 1 - na - na
                     
    # link to the right
    if l < nl -1 and neighbours > 2:
        e[3] = nidx + a
        
        #link to the ang_next - right
         
        if neighbours > 4:
            if a > na -1: 
                e[5] = nidx + na + 1
            else: 
                e[5] = nidx + 1
                
        # link to the prev_ang - right
                
        if neighbours > 6:
            if a > 0:
                e[7] = nidx + na - 1
            else:
                e[7] = nidx + na + na -1
                
    return e
        
        
    
                     
                
                 
