#=========================================================================
# Alu PyMTL Wrapper
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

class ProcDpathAlu( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in0      = InPort ( 32 )
    s.in1      = InPort ( 32 )
    s.fn       = InPort ( 4  )
    s.out      = OutPort( 32 )
    s.ops_eq   = OutPort()
    s.ops_lt   = OutPort()
    s.ops_ltu  = OutPort()

