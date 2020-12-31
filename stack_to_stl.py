# -*- coding: UTF-8 -*-

"""Convert a mandelbulb stack to a surface STL file
"""

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

import os
import pickle

import numpy as np

from skimage.measure import (
  marching_cubes, )

# requires numpy-stl
from stl import mesh

# requires `PyMesh`, which is different from `pymesh` (https://pymesh.readthedocs.io/en/latest/installation.html)
import pymesh

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

PROCESS_LIST = [
  pymesh.remove_isolated_vertices,
  pymesh.remove_duplicated_vertices,
  pymesh.remove_duplicated_faces,
  pymesh.remove_degenerated_triangles, ]

# size of voxel domain in mm
SIZE_XY = 300
SIZE_Z = 75

# hole is 4% of width of voxel domain
HOLE_WIDTH = 0.04

# RESULTS_DIRS = [
#   # 'results/1.0_2.0/',
#   'results/2.0_3.0/',
#   'results/3.0_4.0/',
#   'results/4.0_5.0/', ]

RESULTS_DIRS = [
  'results/2.0_3.1/', ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def pymesh_to_stl( part, stl ):

  faces = part.faces
  verts = part.vertices

  print( 'faces shape: ', faces.shape )
  print( 'verts shape: ', verts.shape )

  # create `numpy-stl` mesh from extracted vertices and faces
  # https://numpy-stl.readthedocs.io/en/latest/usage.html#creating-mesh-objects-from-a-list-of-vertices-and-faces
  m = mesh.Mesh( np.zeros( faces.shape[ 0 ], dtype = mesh.Mesh.dtype ) )
  for i, f in enumerate( faces ):
    for j in range( 3 ):
      m.vectors[ i ][ j ] = verts[ f[ j ], : ]

  # export the STL file of the mesh
  m.save( stl )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def process( _stack, stl ):

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

  pymesh_to_stl(
    part = _m,
    stl = os.path.join( 'results/2.0_3.1/', f'full.stl' ) )

  print( 'Separating mesh into loose pieces' )
  # separate mesh into individual unconnected parts
  parts = pymesh.separate_mesh( _m )

  # # DEBUG
  # output_pkl = os.path.join( 'results/2.0_3.0/', 'parts.pkl' )
  # with open( output_pkl, 'wb' ) as f:
  #   pickle.dump( parts, f )

  # find the part with the most vertices
  nverts = [ part.vertices.shape[ 0 ] for part in parts ]
  # print( sorted( nverts, reverse = True ) )
  # big_idx = np.argmax( nverts )
  # part = parts[ big_idx ]

  sorted_parts = np.argsort( nverts )[ :: -1 ][ :2 ]

  for i, idx in enumerate( sorted_parts ):
    pymesh_to_stl( part = parts[ idx ], stl = os.path.join( 'results/2.0_3.1/', f'part_{i}.stl' ) )

  combined_part = pymesh.boolean(
    mesh_1 = parts[ sorted_parts[ 0 ] ],
    mesh_2 = parts[ sorted_parts[ 1 ] ],
    operation = 'difference'  )

  faces = np.concatenate( [ parts[ sorted_parts[ 0 ] ].faces, parts[ sorted_parts[ 1 ] ].faces ] )
  verts = np.concatenate( [ parts[ sorted_parts[ 0 ] ].vertices, parts[ sorted_parts[ 1 ] ].vertices ] )

  print( 'faces shape: ', faces.shape )
  print( 'verts shape: ', verts.shape )

  # create `numpy-stl` mesh from extracted vertices and faces
  # https://numpy-stl.readthedocs.io/en/latest/usage.html#creating-mesh-objects-from-a-list-of-vertices-and-faces
  m = mesh.Mesh( np.zeros( faces.shape[ 0 ], dtype = mesh.Mesh.dtype ) )
  for i, f in enumerate( faces ):
    for j in range( 3 ):
      m.vectors[ i ][ j ] = verts[ f[ j ], : ]

  # export the STL file of the mesh
  m.save( stl )

  # pymesh_to_stl(
  #   part = combined_part,
  #   stl = os.path.join( 'results/2.0_3.1/', f'combined_part.stl' ) )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

for results_dir in RESULTS_DIRS:

  print( results_dir )

  INPUT_NPY = os.path.join( results_dir, 'stack.npy' )

  OUTPUT_STL = os.path.join( results_dir, 'stack_hole.stl' )

  # load NumPy array of stack
  _stack = np.load( INPUT_NPY )

  N = _stack.shape[ -1 ]
  hw = int( N * HOLE_WIDTH )

  slc = slice(
    ( N - hw - 1) // 2,
    ( N + hw - 1) // 2 )

  hole = np.zeros_like( _stack )
  hole[ :, slc, slc ] = _stack[ :, slc, slc ]

  _stack[ :, slc, slc ] = 0

  # process( _stack = hole, stl = os.path.join( results_dir, 'hole.stl' ) )
  process( _stack = _stack, stl = OUTPUT_STL )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#