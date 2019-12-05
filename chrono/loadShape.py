# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 14:00:40 2019

@author: Admin
"""


import pychrono.core as chrono
import chrono_utils as tool

def loadShape(filepath, contact_method, texture):

    SHAPE_PATH = 'shapes/printed_April18/Cone_23.obj'
    contact_method = chrono.ChMaterialCompositeSMC()
    
    UNIT_FACTOR = 0.01
    
    filepath= tool.obj_from_millimeter(chrono.GetChronoDataPath()+ SHAPE_PATH,
                                       UNIT_FACTOR, f"_{metric}")
    
    shape = chrono.ChBody(contact_method)
    shape.SetBodyFixed(True)
    shape_mesh = chrono.ChObjShapeFile()
    shape_mesh.SetFilename(filepath)
    shape.AddAsset(shape_mesh)
    tmc = chrono.ChTriangleMeshConnected()
    tmc.LoadWavefrontMesh(filepath)
    
    return shape