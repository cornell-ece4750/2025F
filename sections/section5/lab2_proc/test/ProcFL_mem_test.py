#=========================================================================
# ProcFL_test.py
#=========================================================================

import pytest

from pymtl3 import *
from .harness import *
from lab2_proc.ProcFL import ProcFL

#-------------------------------------------------------------------------
# lw
#-------------------------------------------------------------------------

from . import inst_lw

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_lw.gen_basic_test     ) ,
  asm_test( inst_lw.gen_dest_dep_test  ) ,
  asm_test( inst_lw.gen_base_dep_test  ) ,
  asm_test( inst_lw.gen_srcs_dest_test ) ,
  asm_test( inst_lw.gen_addr_test      ) ,
  asm_test( inst_lw.gen_random_test    ) ,
])
def test_lw( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# sw
#-------------------------------------------------------------------------

from . import inst_sw

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_sw.gen_basic_test     ),
])
def test_sw( name, test ):
  run_test( ProcFL, test )

