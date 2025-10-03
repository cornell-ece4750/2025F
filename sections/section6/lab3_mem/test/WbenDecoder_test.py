#=========================================================================
# WbenDecoder_test
#=========================================================================

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim

from lab3_mem.WbenDecoder import WbenDecoder

def test( cmdline_opts ):
  run_test_vector_sim( WbenDecoder(), [
    ('in_ out*'  ),
    [ 0,  0x000f ],
    [ 1,  0x00f0 ],
    [ 2,  0x0f00 ],
    [ 3,  0xf000 ],
  ], cmdline_opts )

