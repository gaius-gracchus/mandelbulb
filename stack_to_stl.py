# -*- coding: UTF-8 -*-

"""Convert a mandelbulb stack to a surface STL file
"""

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

import os

import numpy as np

from skimage.measure import (
  marching_cubes_lewiner, )

# requires numpy-stl
from stl import mesh

# requires `PyMesh`, which is different from `pymesh` (https://pymesh.readthedocs.io/en/latest/installation.html)
import pymesh

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

RESULTS_DIR = 'results/2.0_3.0/'

INPUT_NPY = os.path.join( RESULTS_DIR, 'stack.npy' )

OUTPUT_STL = os.path.join( RESULTS_DIR, 'stack.stl' )

PROCESS_LIST = [
  pymesh.remove_isolated_vertices,
  pymesh.remove_duplicated_vertices,
  pymesh.remove_duplicated_faces,
  pymesh.remove_degenerated_triangles, ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

# load NumPy array of stack
_stack = np.load( INPUT_NPY )

# add base to bottom of stack so the mesh is closed
_stack = np.concatenate(
  [ _stack,  np.ones( ( 1, ) + _stack.shape[ 1: ] ) ],
  axis = 0 )

# rotate stack to get the correct orientation
stack = np.rot90( m = _stack, k = -1, axes = ( 0, 2 ) )

# extract surface mesh objects from the voxel stack
verts, faces, normals, values = marching_cubes_lewiner(
  volume = stack,
  level = np.max( stack ) - 1 )

# create PyMesh mesh
_m = pymesh.form_mesh(vertices = verts, faces = faces )

# cleanup PyMesh mesh
# (https://pymesh.readthedocs.io/en/latest/api_local_mesh_cleanup.html)
for function in PROCESS_LIST:
  _m, info = function( mesh = _m )

# separate mesh into individual unconnected parts
parts = pymesh.separate_mesh( _m )

# find the part with the most vertices
nverts = [ part.vertices.shape[ 0 ] for part in parts ]
big_idx = np.argmax( nverts )
part = parts[ big_idx ]

faces = part.faces
verts = part.vertices

# create `numpy-stl` mesh from extracted vertices and faces
# https://numpy-stl.readthedocs.io/en/latest/usage.html#creating-mesh-objects-from-a-list-of-vertices-and-faces
m = mesh.Mesh( np.zeros( faces.shape[ 0 ], dtype = mesh.Mesh.dtype ) )
for i, f in enumerate( faces ):
  for j in range( 3 ):
    m.vectors[ i ][ j ] = verts[ f[ j ], : ]

# export the STL file of the mesh
m.save( OUTPUT_STL )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#