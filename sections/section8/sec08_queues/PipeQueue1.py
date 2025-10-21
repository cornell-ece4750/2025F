#=========================================================================
# PipeQueue1
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *
from pymtl3.stdlib.stream.ifcs import IStreamIfc, OStreamIfc

class PipeQueue1( VerilogPlaceholder, Component ):
  def construct( s ):
    s.istream = IStreamIfc( Bits32 )
    s.ostream = OStreamIfc( Bits32 )

