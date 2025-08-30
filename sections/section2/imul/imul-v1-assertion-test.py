#=========================================================================
# IntMulScycleV1_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

from IntMulScycleV1 import IntMulScycleV1

#-------------------------------------------------------------------------
# test_basic
#-------------------------------------------------------------------------

def test_basic():

  # Create and elaborate the model

  model = IntMulScycleV1()
  model.elaborate()

  # Apply the Verilog import passes and the default pass group

  model.apply( VerilogPlaceholderPass() )
  model = VerilogTranslationImportPass()( model )
  model.apply( DefaultPassGroup(linetrace=True,vcdwave="imul-v1-simple-test-basic") )

  # Reset simulator

  model.sim_reset()

  # Write inputs and check outputs

  model.in0 @= 2
  model.in1 @= 2
  model.sim_tick()
  assert model.out == 0

  # Tick simulator three more cycles

  model.sim_tick()
  model.sim_tick()
  model.sim_tick()

#-------------------------------------------------------------------------
# test_overflow
#-------------------------------------------------------------------------

def test_overflow():

  # Create and elaborate the model

  model = IntMulScycleV1()
  model.elaborate()

  # Apply the Verilog import passes and the default pass group

  model.apply( VerilogPlaceholderPass() )
  model = VerilogTranslationImportPass()( model )
  model.apply( DefaultPassGroup(linetrace=True,vcdwave="imul-v1-simple-test-overflow") )

  # Reset simulator

  model.sim_reset()

  # Write inputs and check outputs

  model.in0 @= 0x80000001
  model.in1 @= 2
  model.sim_tick()
  assert model.out == 0

  # Tick simulator three more cycles

  model.sim_tick()
  model.sim_tick()
  model.sim_tick()

test_basic()
test_overflow()

