import pychrono as chrono
import pychrono.fea as fea
from scipy.optimize import fmin_bfgs
from scipy.optimize import minimize
import pandas as pd
from shape_energy import shape_energy
import numpy as np
from gen_cylinder import gen_cylinder
import pychrono.irrlicht as chronoirr
import pychrono.mkl as mkl 
import chrono_utils as tools
import math
import geo

# Global -- textile
SENSOR_LEN=10. #in mm. 
ringGap = 12.5 # in mm.
numSensRing = 8
numRings = 8
sleevThickness = 4.215 # in mm

# Global - optimisation algorithm

neighbours = 2
infRadius = 60.
infLength = (numRings - 1) * ringGap

# Global -- 
UNIT_FACTOR= 0.01
metrics = ['mm', 'cm','dm','m']
metric = metrics[int(math.fabs(round(math.log(UNIT_FACTOR,10))))]

#--------------------------------------------------------------------
#chrono setup
chrono.SetChronoDataPath("//smbhome.uscs.susx.ac.uk/lag37/Documents/shapeSim/shapeSensing/chrono/data/")
mysystem = chrono.ChSystemSMC()
mysystem.Set_G_acc(chrono.ChVectorD(0.,0.,0.,))	# set gravity = 0
contact_method = chrono.ChMaterialSurfaceSMC	# set contact method

# ----------------------
# add inference mesh

inf_mesh_init= fea.ChMesh()
inf_mesh = fea.ChMesh()
inf_mesh_big = fea.ChMesh()

# add visualisation information for the mesh init
viz_inf_mesh_init = fea.ChVisualizationFEAmesh(inf_mesh_init)
viz_inf_mesh_init.SetWireframe(True)
viz_inf_mesh_init.SetFEMglyphType(fea.ChVisualizationFEAmesh.E_GLYPH_NODE_DOT_POS)
viz_inf_mesh_init.SetSymbolsThickness(1. * UNIT_FACTOR)
inf_mesh_init.AddAsset(viz_inf_mesh_init)
mysystem.AddMesh(inf_mesh_init)

# information visualisation for inferred mesh 

viz_inf_mesh = fea.ChVisualizationFEAmesh(inf_mesh)
viz_inf_mesh.SetWireframe(True)
viz_inf_mesh.SetFEMglyphType(fea.ChVisualizationFEAmesh.E_GLYPH_NODE_DOT_POS)
viz_inf_mesh.SetSymbolsThickness(0.5 * UNIT_FACTOR)
inf_mesh.AddAsset(viz_inf_mesh)

# information visualisation for mesh big. 

viz_inf_mesh_big = fea.ChVisualizationFEAmesh(inf_mesh_big)
viz_inf_mesh_big.SetWireframe(True)
viz_inf_mesh_big.SetFEMglyphType(fea.ChVisualizationFEAmesh.E_GLYPH_NODE_DOT_POS)
viz_inf_mesh_big.SetSymbolsThickness(2. * UNIT_FACTOR)
inf_mesh_big.AddAsset(viz_inf_mesh_big)
mysystem.AddMesh(inf_mesh_big)


#--------------------------------------------------
# create an Irrlicht to visualize the system

myapp=chronoirr.ChIrrApp(mysystem, ' Mesh Test',
							chronoirr.dimension2du(720,540))
myapp.AddTypicalSky()
myapp.AddTypicalCamera(chronoirr.vector3df(-0.4,-0.3,0.0)) # (1.3*bb_dz,0.,0.) camera location
						#chronoirr.vector3df(0.0, 0.5,-0.1)) # look at location
myapp.AddTypicalLights()
#myapp.SetShowInfos(False)

#
myapp.AssetBindAll()
myapp.AssetUpdateAll()
mysystem.SetupInitial()




						



