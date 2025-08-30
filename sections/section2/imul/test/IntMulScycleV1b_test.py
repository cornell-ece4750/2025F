#=========================================================================
# IntMulScycleV1_test
#=========================================================================

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim

from imul.IntMulScycleV1 import IntMulScycleV1

#-------------------------------------------------------------------------
# test_basic
#-------------------------------------------------------------------------

def test_basic( cmdline_opts ):
  run_test_vector_sim( IntMulScycleV1(), [
    ('in0 in1 out*'),
    [ 2,  2,  '?'  ],
    [ 3,  2,   0   ],
    [ 3,  3,   0   ],
    [ 0,  0,   0   ],
  ], cmdline_opts )

#-------------------------------------------------------------------------
# test_overflow
#-------------------------------------------------------------------------

def test_overflow( cmdline_opts ):
  run_test_vector_sim( IntMulScycleV1(), [
    ('in0         in1 out*'),
    [ 0x80000001, 2,  '?'  ],
    [ 0xc0000002, 4,   0   ],
    [ 0x00000000, 0,   0   ],
  ], cmdline_opts )

