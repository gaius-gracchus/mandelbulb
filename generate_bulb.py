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
N = 250

POW_START = 1.00
POW_STOP = 4.00
DELTA_POW = 0.01

OUTPUT_IMG_FMT = '{:.2f}.png'

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

output_dir = os.path.join(
  RESULTS_DIR,
  f'{POW_START}_{POW_STOP}' )

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

POW_START: {POW_START}
POW_STOP: {POW_STOP}
DELTA_POW: {DELTA_POW}
"""

with open( output_params, 'w' ) as f:
  f.write( params )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

pows = np.arange( POW_START, POW_STOP + DELTA_POW, DELTA_POW )

stack = np.zeros( ( pows.size, N, N ), dtype = np.int32, order = 'F' )

_out = np.zeros( ( N, N ), dtype = np.int32, order = 'F' )

for i, pow in enumerate( pows ):
  mandelpow.main(
    pow = pow,
    z0 = Z0,
    max_iter = MAX_ITER,
    max_value = MAX_VALUE,
    out = _out )

  stack[ i ] = _out

  out = np.asarray( _out * 255. / MAX_ITER, dtype = np.uint8 )
  imageio.imwrite(
    uri = os.path.join( output_img_dir, OUTPUT_IMG_FMT.format( pow ) ),
    im = out )

np.save( file = output_file, arr = stack )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#