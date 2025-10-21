#=========================================================================
# ReplUnit
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

class ReplUnit( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in_ = InPort(32)
    s.out = OutPort(128)

