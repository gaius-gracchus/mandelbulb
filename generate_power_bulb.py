# -*- coding: UTF-8 -*-

"""Generate stack of mandelbrot sets for a range of powers
"""

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

import os

import numpy as np
import imageio

from mandelpow import mandelpow

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

RESULTS_DIR = 'results'

MAX_ITER = 1000
MAX_VALUE = 2.
Z0 = 0.0 + 0.0j
N = 1000

POW_MAGNITUDE = 2.0 + 0.0j
N_THETA = 101

OUTPUT_IMG_FMT = '{:03d}.png'

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

output_dir = os.path.join(
  RESULTS_DIR,
  f'pows_{POW_MAGNITUDE}_{N_THETA}' )

output_img_dir = os.path.join(
  output_dir,
  'images' )

os.makedirs( output_dir, exist_ok = True )
os.makedirs( output_img_dir, exist_ok = True )

output_file = os.path.join(
  output_dir,
  'stack' )

output_params = os.path.join(
  output_dir,
  'params.txt' )

params = f"""
MAX_ITER: {MAX_ITER}
MAX_VALUE: {MAX_VALUE}
Z0: {Z0}
N: {N}

POW_MAGNITUDE: {POW_MAGNITUDE}
N_THETA: {N_THETA}
"""

with open( output_params, 'w' ) as f:
  f.write( params )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

pows = POW_MAGNITUDE * np.exp( np.linspace( 0, 2 * np.pi, N_THETA )[ : -1 ] * 1j )
print( pows )

stack = np.zeros( ( pows.size, N, N ), dtype = np.int32, order = 'F' )

_out = np.zeros( ( N, N ), dtype = np.int32, order = 'F' )

for i, pow in enumerate( pows ):

  print( i, pow )
  mandelpow.main(
    pow = pow,
    z0 = Z0,
    max_iter = MAX_ITER,
    max_value = MAX_VALUE,
    out = _out )

  stack[ i ] = _out

  out = np.asarray( _out * 255. / MAX_ITER, dtype = np.uint8 )
  imageio.imwrite(
    uri = os.path.join( output_img_dir, OUTPUT_IMG_FMT.format( i ) ),
    im = out )

np.save( file = output_file, arr = stack )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#