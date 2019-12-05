# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 11:01:24 2019

@author: Admin
"""

# ------------------------------------------------------------------------------
# Name:        Cloth Simulation
# Purpose: Create a pipeline that:
# # 1. Load and display the shape (mesh defined as .obj file)
# # 2. Create the textile sleeve draping the shape
# # 3. Physical simulation of the sleeve draping the cone +
# #    downsampling to match the number of sensors --> save picture
# # 4. shape optimisation simulation --> save picture
#
# Author:      Sebastien Richoz
#
# Created:     04/04/2019
# Copyright:   Smartsensotics, Wearable Technologies Lab
# ------------------------------------------------------------------------------

import numpy as np
import os
import pychrono.core as chrono
import pychrono.fea as fea
import pychrono.irrlicht as chronoirr
import pychrono.mkl as mkl
from sleeve_shellreissner import SleeveShellReissner
import chrono_utils as tool
from gen_cylinder import gen_cylinder, downsample
from shapeopt_force import shapeopt_force
import math
import geo

print("Cloth Simulation: Physical (pink) and optimisation (green) simulations")

# Change this path to asset path, if running from other working dir.
# It must point to the data folder, containing GUI assets (textures, fonts, meshes, etc.)
chrono.SetChronoDataPath("../data/")

# Global -- Changeable setup
NEIGHBOURS = 4
SAVE_VIDEO = False
# Shape 
SHAPE_PATH = 'shapes/printed_April18/Cone_32.obj'
# Sleeve
NSENSORS_ANGLE = 8
NSENSORS_LENGTH = 8
NNODES_ANGLE = NSENSORS_ANGLE * 2  # Must be a multiple of NSENSOR
NNODES_LENGTH = 2 + NSENSORS_LENGTH * 2  # Must be a multiple of NSENSOR

# Global -- Better not change
SET_MATERIAL = True  # If True, will set a skin material property to the shape (rigid body)
UNIT_FACTOR = 0.01
factor_min_radius = 0.7
metrics = ['mm', 'cm', 'dm', 'm']
metric = metrics[int(math.fabs(round(math.log(UNIT_FACTOR, 10))))]
filename = SHAPE_PATH.split('/')[-1].split('.')[0]
HUMAN_DENSITY = 198.5  # Dkg/m^3

# ---------------------------------------------------------------------
# CHRONO SETUP
# Create the simulation system and add items
mysystem = chrono.ChSystemSMC()
mysystem.Set_G_acc(chrono.ChVectorD(0., 0., 0.))  # Remove gravity
contact_method = chrono.ChMaterialSurface.SMC

# Set global collision margins
chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.0001)
chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.0001)

# ---------------------------------------------------------------------
# SHAPE
# Load and display the shape

# Change the millimeters units into meters
filepath = tool.obj_from_millimeter(chrono.GetChronoDataPath() + SHAPE_PATH, UNIT_FACTOR, f"_{metric}")

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

# ---------------------------------------------------------------------
# SLEEVE
# Create the wrapping sleeve.

# Create the material property of the mesh
rho = 152.2  # 152.2 material density
E = 8e4  # Young's modulus 8e4
nu = 0.5  # 0.5  # Poisson ratio
alpha = 1.0  # 0.3  # shear factor
beta = 0.2  # torque factor
cloth_material = fea.ChMaterialShellReissnerIsothropic(rho, E, nu, alpha, beta)

# Create the mesh. At rest, the radius of the mesh is smaller than the min_radius of the shape
cloth_length = bb_dz + 2 * offset
cloth_radius = factor_min_radius * min_radius
node_mass = 0.1
sleeve_thickness = 0.015
alphadamp = 0.05
sleeve = SleeveShellReissner(cloth_length, cloth_radius, NNODES_ANGLE, NNODES_LENGTH, NEIGHBOURS,
                             cloth_material, node_mass, sleeve_thickness, alphadamp,
                             shift_z=-bb_dz / 2. - offset)

# Set the rest position as the actual position
sleeve.relax()
cloth_mesh = sleeve.get_mesh()

# Add a contact surface mesh with material properties
contact_material = chrono.ChMaterialSurfaceSMC()
# contact_material.SetFriction(0.1)
# contact_material.SetAdhesion(0.5)
contact_material.SetYoungModulus(30e5)
sphere_swept_thickness = 0.008
mcontact = fea.ChContactSurfaceMesh()
cloth_mesh.AddContactSurface(mcontact)
mcontact.AddFacesFromBoundary(sphere_swept_thickness)
mcontact.SetMaterialSurface(contact_material)

# Fix the extremities of the sleeve to the disks
sleeve.fix_extremities(left_cyl, right_cyl, mysystem)

# Extend the sleeve. It will be released after some iterations.
# TODO check for a generic way of computing the expanding force
sleeve.expand(1 / (NNODES_ANGLE * NNODES_LENGTH) * 7000000. * UNIT_FACTOR * bb_dx)

# ---------------------------------------------------------------------
# OPTIMISATION SETUP
# Prepare the visualization of the optimisation algorithm

# Mesh computed by the physical simulation
target_mesh = fea.ChMesh()
# The mesh that will approximate the target mesh
inf_mesh = fea.ChMesh()

# # ---------------------------------------------------------------------
# # VISUALIZATION
mvisualizeClothcoll = fea.ChVisualizationFEAmesh(cloth_mesh)
mvisualizeClothcoll.SetWireframe(True)
mvisualizeClothcoll.SetFEMglyphType(fea.ChVisualizationFEAmesh.E_GLYPH_NODE_DOT_POS)
mvisualizeClothcoll.SetSymbolsThickness(1. * UNIT_FACTOR)
#cloth_mesh.AddAsset(mvisualizeClothcoll)

viz_cloth = fea.ChVisualizationFEAmesh(inf_mesh)
viz_cloth.SetWireframe(True)
viz_cloth.SetFEMglyphType(fea.ChVisualizationFEAmesh.E_GLYPH_NODE_DOT_POS)
viz_cloth.SetFEMdataType(fea.ChVisualizationFEAmesh.E_PLOT_NONE)
viz_cloth.SetSymbolsThickness(0.005)
# viz_cloth.SetDefaultSymbolsColor(chrono.ChColor(0.2,0.3,0.2))  # TODO bug lib
# viz_cloth.SetDefaultMeshColor(chrono.ChColor(0.2,0.3,0.2))  # TODO bug lib
inf_mesh.AddAsset(viz_cloth)

viz_rigid_mesh = fea.ChVisualizationFEAmesh(target_mesh)
viz_rigid_mesh.SetFEMglyphType(fea.ChVisualizationFEAmesh.E_GLYPH_NODE_DOT_POS)
viz_rigid_mesh.SetSymbolsThickness(2. * UNIT_FACTOR)
# viz_rigid_mesh.SetDefaultSymbolsColor(chrono.ChColor(0.2, 0.2, 0.2))  # TODO bug lib
target_mesh.AddAsset(viz_rigid_mesh)

viz_rigid_mesh_beam = fea.ChVisualizationFEAmesh(target_mesh)
viz_rigid_mesh_beam.SetFEMdataType(fea.ChVisualizationFEAmesh.E_PLOT_ELEM_BEAM_MZ)
viz_rigid_mesh_beam.SetColorscaleMinMax(-0.4, 0.4)
viz_rigid_mesh_beam.SetSmoothFaces(True)
viz_rigid_mesh_beam.SetWireframe(False)
target_mesh.AddAsset(viz_rigid_mesh_beam)

# Add mesh to the system
cloth_mesh.SetAutomaticGravity(False)
mysystem.AddMesh(cloth_mesh)
mysystem.AddMesh(inf_mesh)
mysystem.AddMesh(target_mesh)
#
# ---------------------------------------------------------------------
# IRRLICHT
# Create an Irrlicht application to visualize the system
#
myapplication = chronoirr.ChIrrApp(mysystem, 'Cloth Simulation', chronoirr.dimension2du(800, 600)) #1920,1080
myapplication.AddTypicalSky(chrono.GetChronoDataPath() + 'skybox2/')
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


