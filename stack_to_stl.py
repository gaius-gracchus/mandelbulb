# -*- coding: UTF-8 -*-

"""Convert a mandelbulb stack to a surface STL file
"""

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

import os

import numpy as np

from skimage.measure import (
  marching_cubes, )

# requires numpy-stl
from stl import mesh

# requires `PyMesh`, which is different from `pymesh` (https://pymesh.readthedocs.io/en/latest/installation.html)
import pymesh

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

RESULTS_DIR = 'results/1.0_4.0/'

INPUT_NPY = os.path.join( RESULTS_DIR, 'stack.npy' )

OUTPUT_STL = os.path.join( RESULTS_DIR, 'stack_cube.stl' )

PROCESS_LIST = [
  pymesh.remove_isolated_vertices,
  pymesh.remove_duplicated_vertices,
  pymesh.remove_duplicated_faces,
  pymesh.remove_degenerated_triangles, ]

# size of voxel domain in mm
SIZE_XY = 200
SIZE_Z = 100

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

# load NumPy array of stack
_stack = np.load( INPUT_NPY )

# _stack = np.zeros_like( _stack )

# _stack[ 1 : -1, 1 : -1, 1 : -1 ] = 1000

# _tmp = np.ones( ( 1, ) + _stack.shape[ 1: ] )

# # add base to bottom of stack so the mesh is closed
# _stack = np.concatenate(
#   [ _tmp, _stack, _tmp   ],
#   axis = 0 )

# rotate stack to get the correct orientation
stack = np.rot90( m = _stack, k = -1, axes = ( 0, 2 ) )

N_x, N_y, N_z = stack.shape
spacing = ( SIZE_XY / N_x, SIZE_XY / N_y, SIZE_Z / N_z )

print( 'Starting Marching Cubes algorithm' )
# extract surface mesh objects from the voxel stack
verts, faces, normals, values = marching_cubes(
  volume = stack,
  level = np.max( stack ) - 1,
  spacing = spacing, )

# create PyMesh mesh
_m = pymesh.form_mesh(vertices = verts, faces = faces )

print( 'Cleaning up PyMesh mesh' )
# cleanup PyMesh mesh
# (https://pymesh.readthedocs.io/en/latest/api_local_mesh_cleanup.html)
for function in PROCESS_LIST:
  _m, info = function( mesh = _m )

print( 'Separating mesh into loose pieces' )
# separate mesh into individual unconnected parts
parts = pymesh.separate_mesh( _m )

# find the part with the most vertices
nverts = [ part.vertices.shape[ 0 ] for part in parts ]
big_idx = np.argmax( nverts )
part = parts[ big_idx ]

faces = part.faces
verts = part.vertices

print( 'Creating STL file' )

# create `numpy-stl` mesh from extracted vertices and faces
# https://numpy-stl.readthedocs.io/en/latest/usage.html#creating-mesh-objects-from-a-list-of-vertices-and-faces
m = mesh.Mesh( np.zeros( faces.shape[ 0 ], dtype = mesh.Mesh.dtype ) )
for i, f in enumerate( faces ):
  for j in range( 3 ):
    m.vectors[ i ][ j ] = verts[ f[ j ], : ]

# export the STL file of the mesh
m.save( OUTPUT_STL )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#