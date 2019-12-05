# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 11:53:57 2019

@author: Admin
"""

#------------------------------------------------------------------------------
# Name:        pychrono example
# Purpose:
 #
# Author:      Alessandro Tasora
#
 # Created:     1/01/2019
# Copyright:   (c) ProjectChrono 2019
#------------------------------------------------------------------------------
 
 
import pychrono.core as chrono
import pychrono.irrlicht as chronoirr
 
print ("Example: create a system and visualize it in realtime 3D");
    
# Change this path to asset path, if running from other working dir. 
# It must point to the data folder, containing GUI assets (textures, fonts, meshes, etc.)
   19 chrono.SetChronoDataPath("../../../data/")
   20 
   21 # ---------------------------------------------------------------------
   22 #
   23 #  Create the simulation system and add items
   24 #
   25 
   26 mysystem      = chrono.ChSystemNSC()
   27 
   28 # Create a fixed rigid body
   29 
   30 mbody1 = chrono.ChBody()
   31 mbody1.SetBodyFixed(True)
   32 mbody1.SetPos( chrono.ChVectorD(0,0,-0.2))
   33 mysystem.Add(mbody1)
   34 
   35 mboxasset = chrono.ChBoxShape()
   36 mboxasset.GetBoxGeometry().Size = chrono.ChVectorD(0.2,0.5,0.1)
   37 mbody1.AddAsset(mboxasset)
   38 
   39 
   40 
   41 # Create a swinging rigid body
   42 
   43 mbody2 = chrono.ChBody()
   44 mbody2.SetBodyFixed(False)
   45 mysystem.Add(mbody2)
   46 
   47 mboxasset = chrono.ChBoxShape()
   48 mboxasset.GetBoxGeometry().Size = chrono.ChVectorD(0.2,0.5,0.1)
   49 mbody2.AddAsset(mboxasset)
   50 
   51 mboxtexture = chrono.ChTexture()
   52 mboxtexture.SetTextureFilename('../../../data/concrete.jpg')
   53 mbody2.GetAssets().push_back(mboxtexture)
   54 
   55 
   56 # Create a revolute constraint
   57 
   58 mlink = chrono.ChLinkRevolute()
   59 
   60     # the coordinate system of the constraint reference in abs. space:
   61 mframe = chrono.ChFrameD(chrono.ChVectorD(0.1,0.5,0))
   62 
   63     # initialize the constraint telling which part must be connected, and where:
   64 mlink.Initialize(mbody1,mbody2, mframe)
   65 
   66 mysystem.Add(mlink)
   67 
   68 # ---------------------------------------------------------------------
   69 #
   70 #  Create an Irrlicht application to visualize the system
   71 #
   72 
   73 myapplication = chronoirr.ChIrrApp(mysystem, 'PyChrono example', chronoirr.dimension2du(1024,768))
   74 
   75 myapplication.AddTypicalSky()
   76 myapplication.AddTypicalLogo()
   77 myapplication.AddTypicalCamera(chronoirr.vector3df(0.6,0.6,0.8))
   78 myapplication.AddTypicalLights()
   79 
   80             # ==IMPORTANT!== Use this function for adding a ChIrrNodeAsset to all items
   81                         # in the system. These ChIrrNodeAsset assets are 'proxies' to the Irrlicht meshes.
   82                         # If you need a finer control on which item really needs a visualization proxy in
   83                         # Irrlicht, just use application.AssetBind(myitem); on a per-item basis.
   84 
   85 myapplication.AssetBindAll();
   86 
   87                         # ==IMPORTANT!== Use this function for 'converting' into Irrlicht meshes the assets
   88                         # that you added to the bodies into 3D shapes, they can be visualized by Irrlicht!
   89 
   90 myapplication.AssetUpdateAll();
   91 
   92 
   93 # ---------------------------------------------------------------------
   94 #
   95 #  Run the simulation
   96 #
   97 
   98 
   99 myapplication.SetTimestep(0.005)
  100 
  101 
  102 while(myapplication.GetDevice().run()):
  103     myapplication.BeginScene()
  104     myapplication.DrawAll()
  105     myapplication.DoStep()
  106     myapplication.EndScene()
  107 
  108 
  109 
  110 
  111 
© 2016 Project Chrono.
A community project led by the University of Wisconsin-Madison and University of Parma-Italy.

Contact us

ProjectChrono is open-source, hosted at
Github

Generated on Thu Oct 10 2019 13:54:30 for Project Chrono by   doxygen 1.8.9 .