# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 15:23:16 2020

@author: lag37
"""
import math
import pychrono as chrono
import pychrono.fea as fea
import numpy as np
import cylGen
import chrono_utils as tool

class SleeveShellReissner: 
    """
    A sleeve defined as 3D cylinder with elastical properties
    """
    
    minNa = 3   # minimum number of nodes in cross section
    minNl = 2   # minimum number of nodes in lenght
    na = 3
    nl = 2
    nodes = []
    fea_nodes = []
    edges = None        # list of edges
    elements = None     # list of elements
    mesh = None
    length = -1
    radius1 = -1
    radius2 = -1
    shift_x = 0
    shift_y = 0
    
    def __init__(self, length,radius1,radius2,na, nl, neighbours,
                 material = None, node_mass=10., sleeve_thickness=0.002, 
                 alphadamp=0.1):
        
        
        #Handle unrealistic vallues
        if na<3:
            raise ValueError(f"Number of nodes in the circumference"
                             f"must be >= {self.minNa}.")
        if nl < 2:
            raise ValueError(f"Number of nodes in length must be >= {self.minNl}.")
            
        self.na = na
        self.nl = nl
        self.length = length
        self.radius1 = radius1
        self.radius2 = radius2
        #self.shift_x = shift_x
        #self.shift_y = shift_y
        
        # create the nodes and edges arrays using cylGen
        self.nodes, self.edges = cylGen.cylGen(radius1, radius2, length,na,nl,neighbours)
        
        # Crate the mesh made of nodes and elements
        self.mesh = fea.ChMesh()
        
        # Crate FEA nodes
        
        self.fea_nodes = []
        for n in self.nodes:
            nodepos = tool.make_ChVectorD(n)
            noderot = chrono.ChQuaternionD(chrono.QUNIT)
            node = fea.ChNodeFEAxyzrot(chrono.ChFrameD(nodepos,noderot))
            node.SetMass(node_mass)
            self.fea_nodes.append(node)
            self.mesh.AddNode(node)
            
        
        # Create FEA elements
        self.elements = []
        for i in range (nl - 1):
            for j in range(na):
                
                #make elements
                
                elem = fea.ChElementShellReissner4()
                
                if j == na -1:
                # connect last nodes to the first ones
                    elem.SetNodes(
                        self.fea_nodes[(i + 1) * na],   # top right 
                        self.fea_nodes[i * na],         # top left
                        self.fea_nodes[j + i * na],     # bottom left
                        self.fea_nodes[j + (i + 1) * na]# bottom right
                        )
                else:
                    elem.SetNodes(
                        self.fea_nodes[j + 1 + (i + 1) * na],   #top right
                        self.fea_nodes[j + 1 + i * na],         # top left
                        self.fea_nodes[j + i * na],             # bottom left
                        self.fea_nodes[j + (i + 1) * na]        # bottom right
                    )
                    
                if material:
                    elem.AddLayer(sleeve_thickness, 0 * chrono.CH_C_DEG_TO_RAD,
                                  material)
                    elem.SetAlphaDamp(alphadamp)
                    elem.SetAsNeutral()
                    
                    self.mesh.AddElement(elem)
                    self.elements.append(elem)
                    
    
    def get_mesh(self):
        return self.mesh
    
    
    def freeze(self):
        for fn in self.fea_nodes:
            fn.SetFixed(True)
            
    def unfreeze(self):
        for fn in self.fea_nodes:
            fn.SetFixed(False)
    
    def relax(self):
        for fn in self.fea_nodes:
            fn.Relax()
    
                    
                    
        
        

