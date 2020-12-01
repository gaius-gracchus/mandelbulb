# -*- coding: UTF-8 -*-

"""Generate stack of mandelbrot sets for a range of powers
"""

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

import os

import numpy as np
import imageio

from mandelpow import mandelpow

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

OUTPUT_FILE = 'test.png'

MAX_ITER = 1000
MAX_VALUE = 2.
Z0 = 0.0 + 0.0j
N = 1000
_POW = 1.0 + 0.0j

THETA = 0.5
POW = ( _POW.real * np.cos( THETA ) + _POW.imag * np.sin( THETA ) ) + 1j * ( ( _POW.real * np.sin( THETA ) - _POW.imag * np.cos( _POW.imag ) ) )

print( POW )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

_out = np.zeros( ( N, N ), dtype = np.int32, order = 'F' )

mandelpow.main(
  pow = 2.0,
  z0 = Z0,
  max_iter = MAX_ITER,
  max_value = MAX_VALUE,
  out = _out )

out = np.asarray( _out * 255. / MAX_ITER, dtype = np.uint8 )
imageio.imwrite(
  uri = OUTPUT_FILE,
  im = out )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#