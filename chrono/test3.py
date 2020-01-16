# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 17:19:02 2019

@author: lag37
"""

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
chrono.SetChronoDataPath("//smbhome.uscs.susx.ac.uk/lag37/Documents/shapeSim/shapeSensing/chrono/data/")

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




