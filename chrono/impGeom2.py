# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 11:22:39 2019

@author: Admin
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:08:52 2019

@author: Admin
"""


import pychrono.core as chrono
#import pychrono.fea as fea
import pychrono.irrlicht as chronoir

#import numpy as np

# set chrono simulation system
mysystem = chrono.ChSystemSMC()
mysystem.Set_G_acc(chrono.ChVectorD(0.,0.,0.))
contact_method = chrono.ChMaterialSurface.SMC


#   Set the global collision margins. This is specially important for very large 
#   or very small objects. Set this before creating shapes, no before creating 
#   systems
chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.001);
chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.001);

mfloor= chrono.ChBodyEasyBox(30,1,30,1000,True,True)
mfloor.SetBodyFixed(True)
mysystem.Add(mfloor)

print(contact_method)
cp =chrono.SetChronoDataPath("../data/")
shapePath = 'shapes/printed_April18/Cone_32.obj'
#shapePath = "shapes/printed_April18/Cone_32.obj"

#shapePath = "shapes/printed_April18/CL01.STL"

print(chrono.GetChronoDataPath() + shapePath)

tshape = chrono.ChBody(contact_method)

scene_manager=chronoir.ChIrrApp.GetSceneManager();
generic_mesh= scene_manager.getMesh(chrono.GetChronoDataPath()+shapePath);
#sm = chronoir.ChIrrApp.GetSceneManager();
#sm.getMeSH(chrono.GetChronoDataPath() + shapePath)
#

#  Add a collision mesh to the shape

tshape.GetCollisionModel().ClearModel()
tshape.GetCollisionModel().AddTriangleMesh(tmc,True,True)
tshape.GetCollisionModel().BuildModel()
tshape.SetShowCollisionMesh(True)
tshape.SetCollide(False)
#   Add a skin texture





#
# --------------------------------------------------------------------------
# 
# define bounding box, bbox, from imported shape

bbmin, bbmax = chrono.ChVectorD(), chrono.ChVectorD()
shape.GetTotalAABB(bbmin,bbmax)
bbmin, bbmax = eval(str(bbmin)), eval(str(bbmax))
bb_dx=bbmax[0] - bbmin[0]
bb_dy=bbmax[1] - bbmin[1]
bb_dz=bbmax[1] - bbmin[2]

shape.SetPos(chrono.ChVectorD(-bb_dx / 2. - bbmin[0],
                              -bb_dy / 2. - bbmin[1],
                              -bb_dz / 2. - bbmin[2]))
shape.SyncCollisionModels()
mysystem.Add(shape)
mysystem.Add(mfloor)

#bodyA= chrono.ChBodyEasyMesh(chrono.GetChronoDataPath() + shapePath)
#bodyA= chrono.ChBodyEasyMesh(chrono.GetChronoDataPath() + shapePath,
#                             7000,
#                             True,
#                             True)
#
#bodyA.SetPos(chrono.ChVectorD(0.5,1.,0.))
#mysystem.Add(bodyA)
#
#----------------------------------------------------------------------------
#
#  Visuallisation
#


#
#----------------------------------------------------------------------------
#
#   Irrlicht
#   create an Irrlicht application to visualise the system
#

myapplication = chronoir.ChIrrApp(mysystem, 'Test 01',
                                  chronoir.dimension2du(960,540))
myapplication.AddTypicalSky()
myapplication.AddTypicalCamera(chronoir.vector3df(-bb_dx*5000, -bb_dy*5000, -bb_dz*5000))
myapplication.AddTypicalLights()
myapplication.SetPlotCollisionShapes(False)
myapplication.SetPlotCOGFrames(True) # display coord system
myapplication.SetPlotAABB(True)
myapplication.SetShowInfos(False)

#   ==IMPORTANT FOR IRRLICHT TO WORK ===

myapplication.AssetBindAll()
myapplication.AssetUpdateAll()
mysystem.SetupInitial()



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
