#=========================================================================
# WbenDecoder
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

class WbenDecoder( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in_ = InPort(2)
    s.out = OutPort(16)

