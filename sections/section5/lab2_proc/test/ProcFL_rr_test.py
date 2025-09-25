#=========================================================================
# ProcFL_rr_test.py
#=========================================================================

import pytest

from pymtl3 import *
from .harness import *
from lab2_proc.ProcFL import ProcFL

#-------------------------------------------------------------------------
# add
#-------------------------------------------------------------------------

from . import inst_add

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_add.gen_basic_test     ) ,
  asm_test( inst_add.gen_dest_dep_test  ) ,
  asm_test( inst_add.gen_src0_dep_test  ) ,
  asm_test( inst_add.gen_src1_dep_test  ) ,
  asm_test( inst_add.gen_srcs_dep_test  ) ,
  asm_test( inst_add.gen_srcs_dest_test ) ,
  asm_test( inst_add.gen_value_test     ) ,
  asm_test( inst_add.gen_random_test    ) ,
])
def test_add( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# sub
#-------------------------------------------------------------------------

from . import inst_sub

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_sub.gen_basic_test     ) ,
])
def test_sub( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# mul
#-------------------------------------------------------------------------

from . import inst_mul

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_mul.gen_basic_test     ) ,
])
def test_mul( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# and
#-------------------------------------------------------------------------

from . import inst_and

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_and.gen_basic_test     ) ,
  asm_test( inst_and.gen_dest_dep_test  ) ,
  asm_test( inst_and.gen_src0_dep_test  ) ,
  asm_test( inst_and.gen_src1_dep_test  ) ,
  asm_test( inst_and.gen_srcs_dep_test  ) ,
  asm_test( inst_and.gen_srcs_dest_test ) ,
  asm_test( inst_and.gen_value_test     ) ,
  asm_test( inst_and.gen_random_test    ) ,
])
def test_and( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# or
#-------------------------------------------------------------------------

from . import inst_or

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_or.gen_basic_test     ) ,
  asm_test( inst_or.gen_dest_dep_test  ) ,
  asm_test( inst_or.gen_src0_dep_test  ) ,
  asm_test( inst_or.gen_src1_dep_test  ) ,
  asm_test( inst_or.gen_srcs_dep_test  ) ,
  asm_test( inst_or.gen_srcs_dest_test ) ,
  asm_test( inst_or.gen_value_test     ) ,
  asm_test( inst_or.gen_random_test    ) ,
])
def test_or( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# xor
#-------------------------------------------------------------------------

from . import inst_xor

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_xor.gen_basic_test     ) ,
  asm_test( inst_xor.gen_dest_dep_test  ) ,
  asm_test( inst_xor.gen_src0_dep_test  ) ,
  asm_test( inst_xor.gen_src1_dep_test  ) ,
  asm_test( inst_xor.gen_srcs_dep_test  ) ,
  asm_test( inst_xor.gen_srcs_dest_test ) ,
  asm_test( inst_xor.gen_value_test     ) ,
  asm_test( inst_xor.gen_random_test    ) ,
])
def test_xor( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# slt
#-------------------------------------------------------------------------

from . import inst_slt

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_slt.gen_basic_test     ) ,
])
def test_slt( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# sltu
#-------------------------------------------------------------------------

from . import inst_sltu

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_sltu.gen_basic_test     ) ,
])
def test_sltu( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# sra
#-------------------------------------------------------------------------

from . import inst_sra

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_sra.gen_basic_test     ) ,
])
def test_sra( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# srl
#-------------------------------------------------------------------------

from . import inst_srl

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_srl.gen_basic_test     ) ,
])
def test_srl( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# sll
#-------------------------------------------------------------------------

from . import inst_sll

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_sll.gen_basic_test     ) ,
])
def test_sll( name, test ):
  run_test( ProcFL, test )

