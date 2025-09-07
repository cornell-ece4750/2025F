#=========================================================================
# ProcFL_branch_test.py
#=========================================================================

import pytest

from pymtl3 import *
from .harness import *
from lab2_proc.ProcFL import ProcFL

#-------------------------------------------------------------------------
# beq
#-------------------------------------------------------------------------

from . import inst_beq

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_beq.gen_basic_test ) ,
])
def test_beq( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# bne
#-------------------------------------------------------------------------

from . import inst_bne

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_bne.gen_basic_test             ),
  asm_test( inst_bne.gen_src0_dep_taken_test    ),
  asm_test( inst_bne.gen_src0_dep_nottaken_test ),
  asm_test( inst_bne.gen_src1_dep_taken_test    ),
  asm_test( inst_bne.gen_src1_dep_nottaken_test ),
  asm_test( inst_bne.gen_srcs_dep_taken_test    ),
  asm_test( inst_bne.gen_srcs_dep_nottaken_test ),
  asm_test( inst_bne.gen_src0_eq_src1_test      ),
  asm_test( inst_bne.gen_value_test             ),
  asm_test( inst_bne.gen_random_test            ),
])
def test_bne( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# bge
#-------------------------------------------------------------------------

from . import inst_bge

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_bge.gen_basic_test             ),
])
def test_bge( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# bgeu
#-------------------------------------------------------------------------

from . import inst_bgeu

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_bgeu.gen_basic_test             ),
])
def test_bgeu( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# blt
#-------------------------------------------------------------------------

from . import inst_blt

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_blt.gen_basic_test             ),
])
def test_blt( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# bltu
#-------------------------------------------------------------------------

from . import inst_bltu

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_bltu.gen_basic_test             ),
])
def test_bltu( name, test ):
  run_test( ProcFL, test )

