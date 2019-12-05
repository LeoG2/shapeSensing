# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 13:12:27 2019

@author: Admin
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 11:27:31 2019

@author: Admin
"""

import sys
sys.path.append('\SmartSensotics-master\SmartSensotics-master\chrono')
import ChTools as tool

import pychrono.core as chrono
import pychrono.fea as fea
import pychrono.irrlicht as chronoirr
import pychrono.mkl as mkl
from reconstruct_shape_naive import reconstruct_shape
import math

#test visualisation of the mode, whi is not loading other modules

chrono.SetChronoDataPath("../data/")
# create the simulation system and items. 



UNIT_FACTOR = 0.01
RING_GAP = 12.5 * UNIT_FACTOR
SHAPE_THICKNESS = 0.01
SHAPE_PATH = 'shapes/printed_April18/C_29.obj'

metrics = ['mm', 'cm', 'dm', 'm']
metric = metrics[int(math.fabs(round(math.log(UNIT_FACTOR, 10))))]
HUMAN_DENSITY = 198.5  # Dkg/m^3

# -----------------------------------------------------------------------
#
# create the system
mysystem = chrono.ChSystemSMC()
contact_method = chrono.ChMaterialSurface.SMC
mysystem.Set_G_acc(chrono.ChVectorD(0.,0.,0.,))

filepath=tool.obj_from_millimeter(chrono.GetChronoDataPath() + SHAPE_PATH,
                                  UNIT_FACTOR, f"_{metric}")

#import the shape 
shape=tool.load_shape(filepath,contact_method,'textures/skin.jpg')
shape.SetDensity(HUMAN_DENSITY)

# Get shape bounding box dimensions

bbmin,bbmax = chrono.ChVectorD(),chrono.ChVectorD()
shape.GetTotalAABB(bbmin,bbmax)
bbmin,bbmax= eval(str(bbmin)),eval(str(bbmax))
bb_dx=bbmax[0] - bbmin[0]
bb_dy=bbmax[1] - bbmin[1]
bb_dz=bbmax[2] - bbmin[2]
shape.SetMass(100* HUMAN_DENSITY * bb_dx *bb_dy * bb_dz)

# Align shape to centre of axis system

shape.SetPos(chrono.ChVectorD(-bb_dx/2. - bbmin[0],
                              -bb_dy/2. - bbmin[1],
                              -bb_dz/2. - bbmin[2]))

# ----------------------------------------------------------------------------
#
#  Create an Irrlicht application to visualise the system
# 

myapplication = chronoirr.ChIrrApp(mysystem,'Pychrono example',
                                   chronoirr.dimension2du(1027,768))

myapplication.AddTypicalSky()
#myapplication.AddTypicalLogo()
myapplication.AddTypicalCamera(chronoirr.vector3df(0.6,0.6,0.8))
myapplication.AddTypicalLights()

myapplication.AssetBindAll();

myapplication.AssetUpdateAll();

#-----------------------------------------------------------------------------
#
#   Run the simulation
#

myapplication.SetTimestep(0.005)
while(myapplication.GetDevice().run()):
    myapplication.BeginScene()
    myapplication.DrawAll()
    myapplication.DoStep()
    myapplication.EndScene()


