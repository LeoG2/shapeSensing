# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 13:53:15 2020

@author: lag37
"""


import pychrono.core as chrono
import pychrono.irrlicht as chronoirr
import chrono_utils as tool
import math

# ----------------Shape

print(" Chrono import geometry ")

chrono.SetChronoDataPath('//smbhome.uscs.susx.ac.uk/lag37/Documents/shapeSim/shapeSensing/chrono/data/')

SHAPE_PATH = 'shapes/printed_April18/C_29.obj'
UNIT_FACTOR = 0.01
factor_min_radius = 0.7
metrics= ['mm','cm','dm','m']
metric = metrics[int(math.fabs(round(math.log(UNIT_FACTOR, 10))))]
filename = SHAPE_PATH.split('/')[-1].split('.')[0]
HUMAN_DENSITY = 198.5 



# ----------------------------
# CHRONO SETUP
#    create simulation system


mysystem = chrono.ChSystemSMC()
mysystem.Set_G_acc(chrono.ChVectorD(0.,0.,0.,))
contact_method = chrono.ChMaterialSurface.SMC

# set glbal collision margins
chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.0001)
chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.0001)


# chaneg millimeters units into meters

filepath = tool.obj_from_millimeter(chrono.GetChronoDataPath() + SHAPE_PATH, UNIT_FACTOR, f"_{metric}" )

print(filepath)


# Import the shape
shape = tool.load_shape(filepath, contact_method, 'textures/skin.jpg')
shape.SetDensity(HUMAN_DENSITY)

# Get shape bounding box dimensions
bbmin, bbmax = chrono.ChVectorD(), chrono.ChVectorD()
shape.GetTotalAABB(bbmin, bbmax)
bbmin, bbmax = eval(str(bbmin)), eval(str(bbmax))
bb_dx = bbmax[0] - bbmin[0]
bb_dy = bbmax[1] - bbmin[1]
bb_dz = bbmax[2] - bbmin[2]
min_radius = tool.get_shape_min_radius(SHAPE_PATH, bb_dx, bb_dy) * UNIT_FACTOR
offset = 0.02 * bb_dz
shape.SetMass(100 * HUMAN_DENSITY * bb_dx * bb_dy * bb_dz)

# Align shape to the center of axis system
shape.SetPos(chrono.ChVectorD(-bb_dx / 2. - bbmin[0],
                              -bb_dy / 2. - bbmin[1],
                              -bb_dz / 2. - bbmin[2]))
shape.SyncCollisionModels()
mysystem.Add(shape)

# ---------------------------------------------------------------------
# DISKS TO FIX THE SLEEVE
# Add fixed extremities to the shape in order to fix the future mesh.
left_cyl, right_cyl = tool.build_external_cylinder(factor_min_radius * min_radius, bb_dz,
                                                   HUMAN_DENSITY, contact_method, offset)
mysystem.Add(left_cyl)
mysystem.Add(right_cyl)

#
# ---------------------------------------------------------------------
# IRRLICHT
# Create an Irrlicht application to visualize the system
#
myapplication = chronoirr.ChIrrApp(mysystem, 'Cloth Simulation', chronoirr.dimension2du(860, 540))
myapplication.AddTypicalSky(chrono.GetChronoDataPath() + 'skybox/')
myapplication.AddTypicalCamera(chronoirr.vector3df(bb_dz/1.2, 0., 0.))
myapplication.AddTypicalLights()
myapplication.SetPlotCollisionShapes(False)
myapplication.SetPlotCOGFrames(False)  # display coord system
myapplication.SetPlotAABB(False)
myapplication.SetShowInfos(False)

# ==IMPORTANT!== for Irrlicht to work
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

