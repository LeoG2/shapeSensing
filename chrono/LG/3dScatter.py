# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 17:20:45 2019

@author: Admin
"""


import matplotlib.pyplot as plt
from matplotlib import interactive


fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')



ax.scatter(x, y, z, c='r', marker='o')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')



ax.view_init(0,0,180)

plt.show()

