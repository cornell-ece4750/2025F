#=========================================================================
# IntMulScycleV1_test
#=========================================================================

import pytest

from random import randint

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_sim
from pymtl3.stdlib.stream import StreamSourceFL, StreamSinkFL

from imul.IntMulScycleV3 import IntMulScycleV3

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

class TestHarness( Component ):

  def construct( s, imul, imsgs, omsgs ):

    # Instantiate models

    s.src  = StreamSourceFL( Bits64, imsgs )
    s.sink = StreamSinkFL  ( Bits32, omsgs )
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
# test_basic
#-------------------------------------------------------------------------

def test_basic( cmdline_opts ):

  imsgs = [ mk_imsg(2,2), mk_imsg(3,3) ]
  omsgs = [ mk_omsg(4),   mk_omsg(9)   ]

  th = TestHarness( IntMulScycleV3(), imsgs, omsgs )
  run_sim( th, cmdline_opts, duts=['imul'] )

#-------------------------------------------------------------------------
# test_overflow
#-------------------------------------------------------------------------

def test_overflow( cmdline_opts ):

  imsgs = [ mk_imsg(0x80000001,2), mk_imsg(0xc0000002,4) ]
  omsgs = [ mk_omsg(2),            mk_omsg(8)            ]

  th = TestHarness( IntMulScycleV3(), imsgs, omsgs )
  run_sim( th, cmdline_opts, duts=['imul'] )

#-------------------------------------------------------------------------
# test_random
#-------------------------------------------------------------------------

def test_random( cmdline_opts ):

  imsgs = []
  omsgs = []

  for i in range(10):
    a = randint(0,100)
    b = randint(0,100)
    imsgs.extend([ mk_imsg(a,b) ])
    omsgs.extend([ mk_omsg(a*b) ])

  th = TestHarness( IntMulScycleV3(), imsgs, omsgs )
  run_sim( th, cmdline_opts, duts=['imul'] )

