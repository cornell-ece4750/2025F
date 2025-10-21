#=========================================================================
# simple_test.py
#=========================================================================
# This is primarily just for playing around with little transaction
# sequences.

from pymtl3 import *

from pymtl3.stdlib.mem import MemoryFL, mk_mem_msg, MemMsgType
from pymtl3.stdlib.stream import StreamSourceFL, StreamSinkFL
from pymtl3.stdlib.test_utils import run_sim

from lab3_mem.CacheFL     import CacheFL
from lab3_mem.CacheSimple import CacheSimple

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
# TestHarness
#-------------------------------------------------------------------------

class TestHarness( Component ):

  def construct( s, cache_cls, imsgs, omsgs ):

    # Instantiate models

    s.src   = StreamSourceFL( CacheReqType, imsgs )
    s.cache = cache_cls
    s.mem   = MemoryFL( 1, [(MemReqType,MemRespType)] )
    s.sink  = StreamSinkFL( CacheRespType, omsgs )

    # Connect

    s.src.ostream     //= s.cache.proc2cache.reqstream
    s.sink.istream    //= s.cache.proc2cache.respstream
    s.cache.cache2mem //= s.mem.ifc[0]

  def done( s ):
    return s.src.done() and s.sink.done()

  def line_trace( s ):
    return s.src.line_trace() + " > " + s.cache.line_trace() + " > " \
         + s.mem.line_trace() + " > " + s.sink.line_trace()

#----------------------------------------------------------------------
# test
#----------------------------------------------------------------------

def test( cmdline_opts ):

  msgs = [
    #    type  opq  addr    len data                type  opq  test len data
    req( 'in', 0x0, 0x1000, 0, 0xdeadbeef ), resp( 'in',  0x0, 0,   0,  0          ),
  ]

  model = TestHarness( CacheFL(), msgs[::2], msgs[1::2] )

  run_sim( model, cmdline_opts, duts=['cache'] )

