# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 13:50:40 2020

@author: lag37
"""

import pychrono.fea as fea
from sleeveSR import SleeveShellReissner
import pychrono as chrono



# global variables 
neighbours = 4

#global variables (constants), 

SET_Material = False  # if true, will set a skin material property to the shape 
UNIT_FACTOR = 0.01
factor_min_radisu = 0.7
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

mysystem = chrono.ChSystemSMC()
mysystem.Set_G_acc(chrono.ChVectorD(0.,0.,0.)) # set grity to 0
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

sleeve = SleeveShellReissner(cloth_radius1,cloth_radius2,cloth_length,
                             neighbours,10,10, cloth_material, node_mass,
                             sleeve_thickness,alphaDamp)

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
# Prepare the visualisation ofr the optimisation algorithm

# Mesh computed by physical simulation

targetMesh= fea.ChMesh()

# inference mesh

infMesh = fea.ChMesh()




###  -------------------------------------------------------------------------

# # Visualisation

visCloth = fea.ChVisualizationFEAmesh(cloth_mesh)
visCloth.SetWireframe(True)
visCloth.SetFEMglyphType(fea.ChVisualizationFEAmesh.E_GLYPH_NODE_DOT_POS)
visCloth.SetSymbolsThickness(1. * 2.)

visTmesh= fea.ChVisualizationFEAmesh(targetMesh)
visTmesh.SetWireframe(True)
visTmesh.SetFEMglyphType(fea.ChVisualizationFEAmesh.E_GLYPH_NODE_DOT_POS)
visTmesh.SetFEMdataType(fea.ChVisualizationFEAmesh.E_PLOT_NONE)
visTmesh.SetSymbolsThickness(0.005) 
#visTmesh.SetDefaultSymbolsColor(chrono.ChColor(0.2,0.3,0.2)) #BUG??
#visTmesh.SetDefaultMeshColor(chrono.ChColor(0.2,0.3,0.2)) # bug? library

infMesh.AddAsset(visTmesh)


# Add mesh to the system
#cloth_mesh.SetAutomaticGravity(False)



   






