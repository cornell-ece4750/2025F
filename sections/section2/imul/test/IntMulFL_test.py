#=========================================================================
# IntMulFL_test
#=========================================================================

import pytest

from random import randint

from pymtl3 import *
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim
from pymtl3.stdlib.stream import StreamSourceFL, StreamSinkFL

from imul.IntMulFL import IntMulFL

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

class TestHarness( Component ):

  def construct( s, imul, src_msgs, sink_msgs, delay=0 ):

    # Instantiate models

    s.src  = StreamSourceFL( Bits64, src_msgs  )
    s.sink = StreamSinkFL  ( Bits32, sink_msgs,
                             initial_delay=delay, interval_delay=delay )
    s.imul = imul

    # Connect

    s.src.ostream  //= s.imul.istream
    s.imul.ostream //= s.sink.istream

  def done( s ):
    return s.src.done() and s.sink.done()

  def line_trace( s ):
    return s.src.line_trace() + " > " + s.imul.line_trace() + " > " + s.sink.line_trace()

#-------------------------------------------------------------------------
# mk_imsg/mk_omsg
#-------------------------------------------------------------------------
# Make input/output msgs, truncate ints to ensure they fit in 32 bits.

def mk_imsg( a, b ):
  return concat( Bits32( a, trunc_int=True ), Bits32( b, trunc_int=True ) )

def mk_omsg( a ):
  return Bits32( a, trunc_int=True )

#-------------------------------------------------------------------------
# test msgs
#-------------------------------------------------------------------------

basic_msgs = [
  mk_imsg(2,2), mk_omsg(4),
  mk_imsg(3,3), mk_omsg(9),
]

overflow_msgs = [
  mk_imsg(0x80000001,2), mk_omsg(2),
  mk_imsg(0xc0000002,4), mk_omsg(8),
]

random_msgs  = []
for i in range(10):
  a = randint(0,100)
  b = randint(0,100)
  random_msgs.extend ([ mk_imsg(a,b), mk_omsg(a*b) ])

#-------------------------------------------------------------------------
# Test Case Table
#-------------------------------------------------------------------------

test_case_table = mk_test_case_table([
  (                  "msgs          delay"),
  [ "basic",         basic_msgs,    0     ],
  [ "overflow",      overflow_msgs, 0     ],
  [ "random",        random_msgs,   0     ],
  [ "random_delay1", random_msgs,   1     ],
  [ "random_delay3", random_msgs,   3     ],
])

#-------------------------------------------------------------------------
# run tests
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table )
def test( test_params, cmdline_opts ):

  src_msgs  = test_params.msgs[::2]
  sink_msgs = test_params.msgs[1::2]
  delay     = test_params.delay

  th = TestHarness( IntMulFL(), src_msgs, sink_msgs, delay )
  run_sim( th, cmdline_opts, duts=['imul'] )

