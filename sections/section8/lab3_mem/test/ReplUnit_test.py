#=========================================================================
# ReplUnit_test
#=========================================================================

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim

from lab3_mem.ReplUnit import ReplUnit

def test( cmdline_opts ):
  run_test_vector_sim( ReplUnit(), [
    ('in_         out*'  ),
    [ 0x00000000, 0x00000000000000000000000000000000 ],
    [ 0x00000001, 0x00000001000000010000000100000001 ],
    [ 0x80000000, 0x80000000800000008000000080000000 ],
    [ 0xdeadbeef, 0xdeadbeefdeadbeefdeadbeefdeadbeef ],
  ], cmdline_opts )

