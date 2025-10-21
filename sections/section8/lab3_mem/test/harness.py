#=========================================================================
# harness.py
#=========================================================================
# Message types, test harness, and run test function for testing.

import struct

from pymtl3 import *

from pymtl3.stdlib.mem        import MemoryFL, mk_mem_msg, MemMsgType
from pymtl3.stdlib.stream     import StreamSourceFL, StreamSinkFL
from pymtl3.stdlib.test_utils import run_sim

#-------------------------------------------------------------------------
# Message Types
#-------------------------------------------------------------------------

CacheReqType, CacheRespType = mk_mem_msg( 8, 32, 32  )
MemReqType,   MemRespType   = mk_mem_msg( 8, 32, 128 )

def req( type_, opaque, addr, len, data ):
  if   type_ == 'rd': type_ = MemMsgType.READ
  elif type_ == 'wr': type_ = MemMsgType.WRITE
  elif type_ == 'in': type_ = MemMsgType.WRITE_INIT

  return CacheReqType( type_, opaque, addr, len, data)

def resp( type_, opaque, test, len, data ):
  if   type_ == 'rd': type_ = MemMsgType.READ
  elif type_ == 'wr': type_ = MemMsgType.WRITE
  elif type_ == 'in': type_ = MemMsgType.WRITE_INIT

  return CacheRespType( type_, opaque, test, len, data )

#-------------------------------------------------------------------------
# compare_cacheresp
#-------------------------------------------------------------------------
# The test field in the cache response is used to indicate if the
# corresponding memory access resulted in a hit or a miss. However, the
# FL model always sets the test field to zero since it does not track
# hits/misses. So we need to do something special to ignore the test
# field when using the FL model. To do this, we can pass in a specialized
# comparison function to the StreamSinkFL. By default we pass in the
# following comparison function which does indeed check the test bit.

def compare_cacheresp( msg, ref ):

  # check type, len, opaque, data fields

  if msg.type_ != ref.type_:
    return False

  if msg.len != ref.len:
    return False

  if msg.opaque != ref.opaque:
    return False

  if msg.test != ref.test:
    return False

  if ref.data != msg.data:
    return False

  # do not check the test field

  return True

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

class TestHarness( Component ):

  def construct( s, dut, cmp_fn=compare_cacheresp ):

    # Instantiate models

    s.src   = StreamSourceFL( CacheReqType )
    s.cache = dut
    s.mem   = MemoryFL( 1, [(MemReqType,MemRespType)] )
    s.sink  = StreamSinkFL( CacheRespType, cmp_fn=cmp_fn )

    # Connect

    s.src.ostream     //= s.cache.proc2cache.reqstream
    s.sink.istream    //= s.cache.proc2cache.respstream
    s.cache.cache2mem //= s.mem.ifc[0]

  def load( s, addrs, data_ints ):
    for addr, data_int in zip( addrs, data_ints ):
      data_bytes_a = bytearray()
      data_bytes_a.extend( struct.pack("<I",data_int) )
      s.mem.write_mem( addr, data_bytes_a )

  def done( s ):
    return s.src.done() and s.sink.done()

  def line_trace( s ):
    return s.src.line_trace() + " > " + s.cache.line_trace() + " > " \
         + s.mem.line_trace() + " > " + s.sink.line_trace()

#-------------------------------------------------------------------------
# run_test
#-------------------------------------------------------------------------

def run_test( CacheModel, test_params, cmdline_opts, cmp_fun=compare_cacheresp ):

  # Instantiate test harness

  th = TestHarness( CacheModel, cmp_fun )

  # Generate messages

  msgs = test_params.msg_func()

  # Set parameters

  th.set_param("top.src.construct",
    msgs=msgs[::2],
    initial_delay=test_params.src+3,
    interval_delay=test_params.src )

  th.set_param("top.sink.construct",
    msgs=msgs[1::2],
    initial_delay=test_params.sink+3,
    interval_delay=test_params.sink )

  th.set_param( "top.mem.construct",
    stall_prob=test_params.stall,
    extra_latency=test_params.lat )

  th.elaborate()

  # Load memory before the test

  if test_params.mem_data_func != None:
    mem = test_params.mem_data_func()
    th.load( mem[::2], mem[1::2] )

  # Run the test

  run_sim( th, cmdline_opts, duts=['cache'] )

