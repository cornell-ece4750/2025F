#=========================================================================
# PipeQueue1_test.py
#=========================================================================

import pytest

from random import randint

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_sim
from pymtl3.stdlib.stream import StreamSourceFL, StreamSinkFL

from sec08_queues.PipeQueue1 import PipeQueue1

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

class TestHarness( Component ):

  def construct( s, queue, imsgs, omsgs, delay=0 ):

    # Instantiate models

    s.src  = StreamSourceFL( Bits32, imsgs )
    s.sink = StreamSinkFL  ( Bits32, omsgs,
                             initial_delay=delay, interval_delay=delay )
    s.queue = queue

    # Connect

    s.src.ostream   //= s.queue.istream
    s.queue.ostream //= s.sink.istream

  def done( s ):
    return s.src.done() and s.sink.done()

  def line_trace( s ):
    return s.src.line_trace() + " > () > " + s.sink.line_trace()

#-------------------------------------------------------------------------
# test
#-------------------------------------------------------------------------

def test( cmdline_opts ):

  msgs = [ Bits32(i) for i in range(5) ]

  th = TestHarness( PipeQueue1(), msgs, msgs )
  run_sim( th, cmdline_opts, duts=['queue'] )

#-------------------------------------------------------------------------
# test_delay
#-------------------------------------------------------------------------

def test_delay( cmdline_opts ):

  msgs = [ Bits32(i) for i in range(5) ]

  th = TestHarness( PipeQueue1(), msgs, msgs, 3 )
  run_sim( th, cmdline_opts, duts=['queue'] )

