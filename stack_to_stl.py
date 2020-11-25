# -*- coding: UTF-8 -*-

"""Convert a mandelbulb stack to a surface STL file
"""

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

import numpy as np

from skimage.measure import (
  marching_cubes_lewiner, )

# requires numpy-stl
from stl import mesh

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

INPUT_NPY = 'results/1.0_5.0/stack.npy'

OUTPUT_STL = 'results/1.0_5.0/stack.stl'

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

stack = np.load( INPUT_NPY )

verts, faces, normals, values = marching_cubes_lewiner(
  volume = stack,
  level = np.max( stack ) - 1 )

# https://numpy-stl.readthedocs.io/en/latest/usage.html#creating-mesh-objects-from-a-list-of-vertices-and-faces
m = mesh.Mesh( np.zeros( faces.shape[ 0 ], dtype = mesh.Mesh.dtype ) )
for i, f in enumerate( faces ):
  for j in range( 3 ):
    m.vectors[ i ][ j ] = verts[ f[ j ], : ]

m.save( OUTPUT_STL )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#