#=========================================================================
# IntMulScycleV1_test
#=========================================================================

import pytest

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim

from imul.IntMulScycleV1 import IntMulScycleV1

#-------------------------------------------------------------------------
# basic
#-------------------------------------------------------------------------

basic_test_vectors = [
  ('in0 in1 out*'),
  [ 2,  2,  '?'  ],
  [ 3,  2,   0   ],
  [ 3,  3,   0   ],
  [ 0,  0,   0   ],
]

#-------------------------------------------------------------------------
# overflow
#-------------------------------------------------------------------------

overflow_test_vectors = [
  ('in0         in1 out*'),
  [ 0x80000001, 2,  '?'  ],
  [ 0xc0000002, 4,   0   ],
  [ 0x00000000, 0,   0   ],
]

#-------------------------------------------------------------------------
# test
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "test_vectors", [
  basic_test_vectors,
  overflow_test_vectors
])
def test( test_vectors, cmdline_opts ):
    run_test_vector_sim( IntMulScycleV1(), test_vectors, cmdline_opts )

