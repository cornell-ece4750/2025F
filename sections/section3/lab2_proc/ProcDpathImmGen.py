#=========================================================================
# ImmGen PyMTL Wrapper
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

class ProcDpathImmGen( VerilogPlaceholder, Component ):
  def construct( s ):
    s.imm_type = InPort ( 3  )
    s.inst     = InPort ( 32 )
    s.imm      = OutPort( 32 )

