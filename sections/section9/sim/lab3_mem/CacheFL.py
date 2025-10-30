#=========================================================================
# Blocking Cache FL Model
#=========================================================================
# A function level cache model which only passes cache requests and
# responses to the memory.

from pymtl3 import *
from pymtl3.stdlib.stream      import IStreamDeqAdapterFL, OStreamEnqAdapterFL
from pymtl3.stdlib.mem.ifcs    import MemRequesterIfc, MemResponderIfc
from pymtl3.stdlib.mem         import mk_mem_msg, MemMsgType, MemRequesterAdapterFL

class CacheFL( Component ):

  def construct( s, p_num_banks=1 ):

    # Interface

    CacheReqType, CacheRespType = mk_mem_msg( 8, 32, 32  )
    MemReqType,   MemRespType   = mk_mem_msg( 8, 32, 128 )

    s.proc2cache = MemResponderIfc( CacheReqType, CacheRespType )
    s.cache2mem  = MemRequesterIfc( MemReqType,   MemRespType   )

    # Proc <-> Cache Adapters

    s.cache_reqstream_q  = IStreamDeqAdapterFL( CacheReqType  )
    s.cache_respstream_q = OStreamEnqAdapterFL( CacheRespType )

    connect( s.proc2cache.reqstream, s.cache_reqstream_q.istream   )
    connect( s.cache_respstream_q.ostream, s.proc2cache.respstream )

    # Cache <-> Memory Adapters

    s.mem_adapter = MemRequesterAdapterFL( MemReqType, MemRespType )

    connect( s.cache2mem, s.mem_adapter.requester )

    # Logic

    @update_once
    def logic():

      # Process cache request if input and output stream are both ready

      if s.cache_reqstream_q.deq.rdy() and s.cache_respstream_q.enq.rdy():

        # Dequeue cache request

        cachereq = s.cache_reqstream_q.deq()

        # By default the read data is always zero (i.e., for writes)

        data = Bits32(0)

        # Handle write transactions

        if (    ( cachereq.type_ == MemMsgType.WRITE_INIT )
             or ( cachereq.type_ == MemMsgType.WRITE ) ):
          s.mem_adapter.write( cachereq.addr, 4, cachereq.data )

        # Handle read transactions

        elif ( cachereq.type_ == MemMsgType.READ ):
          data = s.mem_adapter.read( cachereq.addr, 4 )

        # Create appropriate cache response

        cacheresp = CacheRespType( cachereq.type_, cachereq.opaque,
                                   Bits2(0), cachereq.len, data )

        # Enqueue cache response on output stream

        s.cache_respstream_q.enq( cacheresp )

  def line_trace(s):
    return "()"

