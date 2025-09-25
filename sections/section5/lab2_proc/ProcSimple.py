#=========================================================================
# ProcSimple PyMTL Wrapper
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *
from pymtl3.stdlib.stream.ifcs import IStreamIfc, OStreamIfc
from pymtl3.stdlib.mem.ifcs    import MemRequesterIfc
from pymtl3.stdlib.mem         import mk_mem_msg

class ProcSimple( VerilogPlaceholder, Component ):
  def construct( s ):

    req_class, resp_class = mk_mem_msg( 8, 32, 32 )

    s.mngr2proc   = IStreamIfc( Bits32 )
    s.proc2mngr   = OStreamIfc( Bits32 )
    s.imem        = MemRequesterIfc( req_class, resp_class )
    s.dmem        = MemRequesterIfc( req_class, resp_class )
    s.core_id     = InPort(32)
    s.commit_inst = OutPort()
    s.stats_en    = OutPort()

