#=========================================================================
# SingleCoreSysFL
#=========================================================================

from pymtl3 import *

from pymtl3.stdlib.stream.ifcs import IStreamIfc, OStreamIfc
from pymtl3.stdlib.mem.ifcs    import MemRequesterIfc
from pymtl3.stdlib.mem         import mk_mem_msg

from lab2_proc.ProcFL import ProcFL
from lab3_mem.CacheFL import CacheFL

class SingleCoreSysFL( Component ):

  def construct( s ):

    MemReqType, MemRespType = mk_mem_msg( 8, 32, 128 )

    # Interface

    s.mngr2proc     = IStreamIfc( Bits32 )
    s.proc2mngr     = OStreamIfc( Bits32 )
    s.imem          = MemRequesterIfc( MemReqType, MemRespType )
    s.dmem          = MemRequesterIfc( MemReqType, MemRespType )

    s.stats_en      = OutPort()
    s.commit_inst   = OutPort()
    s.icache_access = OutPort()
    s.icache_miss   = OutPort()
    s.dcache_access = OutPort()
    s.dcache_miss   = OutPort()

    # Instantiate processor and two caches

    s.proc   = ProcFL()
    s.icache = CacheFL()
    s.dcache = CacheFL()

    # Connect proc2mngr and mngr2proc interfaces

    s.mngr2proc //= s.proc.mngr2proc
    s.proc2mngr //= s.proc.proc2mngr

    # Connect processors <-> caches

    s.proc.imem //= s.icache.proc2cache
    s.proc.dmem //= s.dcache.proc2cache

    # Connect caches <-> memory

    s.imem //= s.icache.cache2mem
    s.dmem //= s.dcache.cache2mem

    # Bring the stats enable up to the top level

    s.stats_en      //= s.proc.stats_en
    s.commit_inst   //= s.proc.commit_inst
    s.icache_access //= 0
    s.icache_miss   //= 0
    s.dcache_access //= 0
    s.dcache_miss   //= 0

  def line_trace( s ):
    return s.proc.line_trace()

