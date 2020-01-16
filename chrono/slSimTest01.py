# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 13:50:40 2020

@author: lag37
"""

import numpy as np
import pychrono.core as chrono
import pychrono.fea as fea
import pychrono.irrlicht as chronoirr
import pychrono.mkl as mkl
from sleeveSR import SleeveShellReissner
#from sleeve_shellreissner import SleeveShellReissner
import math
import geo

# change this path to asset path, if running from other working dir.
# It must point to the data folder, containing GUI assets 
# (textures, fonts, meshes, etc.)
chrono.SetChronoDataPath("//smbhome.uscs.susx.ac.uk/lag37/Documents/shapeSim/shapeSensing/chrono/data/")


# global variables 
neighbours = 4

#global variables (constants keep constant), 

SET_Material = False  # if true, will set a skin material property to the shape 
UNIT_FACTOR = 0.01
factor_min_radius = 0.7
metrics = ['mm','cm','dm','m']


sensorsCrossSection = 8
sensorsLength = 8
nNodesCSection = sensorsCrossSection * 2    # must be a multiple of sensors
nNodesLength = 2 + sensorsLength * 2        # must be a multiple of sensors
shift_x = 0
shift_y = 0
shift_z = 0

# ----------------------------------------------------------------------------

# CHRONO SETUP
# Create a simulation system an add items
# Create a Chrono::Engine physical system
mysystem = chrono.ChSystemSMC()
mysystem.Set_G_acc(chrono.ChVectorD(0.,0.,0.)) # set gravity to 0
contact_method = chrono.ChMaterialSurface.SMC


#set global collision margins
chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.0001)
chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.0001)

# --------------------------------------------------------------------------
# Define the mesh shape and create the mesh

# create material property for the mesh
rho = 152.2 # material density
E = 8e4     # Young's modulus
nu = 0.5    # Poisson's ration
alpha = 1.0 # 0.3 shear factor
beta = 0.2  # torque factor

cloth_material = fea.ChMaterialShellReissnerIsothropic(rho, E, nu,alpha,beta)

# create the mesh. At rest of the mesh is smaller than the min radius of the 
# shape


cloth_length = 140
cloth_radius1=30
cloth_radius2=30
node_mass = 0.1
sleeve_thickness = 0.015
alphaDamp = 0.05

sleeve = SleeveShellReissner(cloth_length, cloth_radius1,cloth_radius2,
                             10,10, neighbours, cloth_material, node_mass,
                             sleeve_thickness,alphaDamp)

# sleeve = SleeveShellReissner(cloth_length, cloth_radius1,
#                              neighbours,10,10, cloth_material, node_mass,
#                              sleeve_thickness,alphaDamp, shift_x=0, shift_y=0, shift_z=0 )

# set actual position as rest position
sleeve.relax()
cloth_mesh = sleeve.get_mesh()

#add contact surface mesh with material properties

contact_material = chrono.ChMaterialSurfaceSMC()
#contact_material.SetFriction(0.1)
#contact_material.SetAdhesion(0.5)
contact_material.SetYoungModulus(30e5)
sphere_swept_thickness = 0.008
mcontact = fea.ChContactSurfaceMesh()
cloth_mesh.AddContactSurface(mcontact)
mcontact.AddFacesFromBoundary(sphere_swept_thickness)
mcontact.SetMaterialSurface(contact_material)


# ---------------------------------------------------------------------------
# Optimisation set up
# Prepare the visualisation for the optimisation algorithm
# create meshes, containers for groups of elements#
# and referenced nodes

# Mesh computed by physical simulation

targetMesh= fea.ChMesh()

# inference mesh

infMesh = fea.ChMesh()


# We do not want gravity effect on FEA elements

targetMesh.SetAutomaticGravity(False)

path=chrono.GetChronoDataPath()
print(path)


###  -------------------------------------------------------------------------

# ==Asset== attach a visualisation of the FEM mesh. 
# This will automaticaly update a triangle mesh (a ChTriangleMeshShape asset
# that is internally managed) by setting ptoper coordinates and vertex 
# as in the FEM elements.

# # Visualisation


visCloth = fea.ChVisualizationFEAmesh(cloth_mesh)
visCloth.SetWireframe(True)
visCloth.SetFEMglyphType(fea.ChVisualizationFEAmesh.E_GLYPH_NODE_DOT_POS)
#visCloth.SetFEMdataType(fea.ChVisualizationFEAmesh.E_PLOT_NONE)
visCloth.SetSymbolsThickness(1.)
#cloth_mesh.AddAsset(visCloth)

# visInfMesh=fea.ChVisualizationFEAmesh(infMesh)
# visInfMesh.SetWireframe(True)
# visInfMesh.SetFEMglyphType(fea.ChVisualizationFEAmesh.E_GLYPH_NODE_DOT_POS)
# visInfMesh.SetFEMdataType(fea.ChVisualizationFEAmesh.E_PLOT_NONE)
# infMesh.AddAsset(visInfMesh)


visTmesh= fea.ChVisualizationFEAmesh(targetMesh)
visTmesh.SetWireframe(True)
visTmesh.SetFEMglyphType(fea.ChVisualizationFEAmesh.E_GLYPH_NODE_DOT_POS)
visTmesh.SetFEMdataType(fea.ChVisualizationFEAmesh.E_PLOT_NONE)
visTmesh.SetSymbolsThickness(0.005) 
#visTmesh.SetDefaultSymbolsColor(chrono.ChColor(0.2,0.3,0.2)) #BUG??
#visTmesh.SetDefaultMeshColor(chrono.ChColor(0.2,0.3,0.2)) # bug? library
targetMesh.AddAsset(visTmesh)

# Add mesh to the system
#cloth_mesh.SetAutomaticGravity(False)
#mysystem.Add(targetMesh)

#mysystem.AddMesh(cloth_mesh)
#mysystem.AddMesh(targetMesh)
# 
# --------------------------------------------------------------------------
# IRRLICHT
# create an Irrlich application to visualize the system

# Create an Irrlich visualisation (open the Irrlichr device, 
# bind a simple user interface, etc. etc.)

myapplication = chronoirr.ChIrrApp(mysystem, 'Mesh Simulation Test', 
                                  chronoirr.dimension2du(800,500))
myapplication.AddTypicalSky(chrono.GetChronoDataPath() + 'skybox/')
myapplication.AddTypicalCamera(chronoirr.vector3df(1.3,0.,0.))
myapplication.AddTypicalLights()
myapplication.SetPlotCollisionShapes(False)
myapplication.SetPlotCOGFrames(False)
myapplication.SetPlotAABB(False)
myapplication.SetShowInfos(False)

## == IMPORTANT! == this function for adding a ChIrrNodeAsset to all 
# items in the system. These ChIrrNodeAsset assets are 'proxies' to the 
# Irrlicht meshes

myapplication.AssetBindAll()

## == IMPORTANT! == Use this function for 'converting' into Irrlicht meshes 
# the assets added to the bodies into 3D shapes, they can be vsiualised 
# by Irrlicht! 
myapplication.AssetUpdateAll()

# Mark completion of the system construction.
mysystem.SetupInitial()

# ---------------------------------------------------------------------------
# SIMULATION 
# Run the simulation

# Change solver from the default SOR to the MKL Pardiso, more precise for fea
# msolver = mkl.ChSolverMKLcsm()
# mysystem.SetSolver(msolver)
# myapplication.SetTimestep(0.001)

# step = 0
# im_step = 0 # inverse modelling step
# threshold = 0.00007  # minimum value to detect stabilisation
# # minimum length to be reached by the optimisation algorithm to detect
# #  stabilisation
# inv_mod_threshold = 0.001

# is_inverse_modeling = False
# is_detecting_stab = False
# is_inv_mode_stabilised = False
# targetNodes = []
# targetEdges = []
# clothNodes = []
# clothEdges = []
# current_cloth_nodes_pos = []

# #save first image 
# #myapplication.SetVideoframeSave(True)




# # while(myapplication.GetDevice().run()):
#     print('step', step)
#     myapplication.BeginScene()
#     myapplication.DrawAll()
#     myapplication.DoStep()
#     myapplication.EndScene()
    
    # Save figure of the shape only
    


   






