#=========================================================================
# ProcFL_alu_test.py
#=========================================================================

import pytest

from pymtl3 import *
from .harness import *
from lab2_proc.ProcFL import ProcFL

#-------------------------------------------------------------------------
# addi
#-------------------------------------------------------------------------

from . import inst_addi

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_addi.gen_basic_test     ) ,
  asm_test( inst_addi.gen_dest_dep_test  ),
  asm_test( inst_addi.gen_src_dep_test   ),
  asm_test( inst_addi.gen_srcs_dest_test ),
  asm_test( inst_addi.gen_value_test     ),
  asm_test( inst_addi.gen_random_test    ),
])
def test_addi( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# andi
#-------------------------------------------------------------------------

from . import inst_andi

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_andi.gen_basic_test     ) ,
  asm_test( inst_andi.gen_dest_dep_test  ) ,
  asm_test( inst_andi.gen_src_dep_test   ) ,
  asm_test( inst_andi.gen_srcs_dest_test ) ,
  asm_test( inst_andi.gen_value_test     ) ,
  asm_test( inst_andi.gen_random_test    ) ,
])
def test_andi( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# ori
#-------------------------------------------------------------------------

from . import inst_ori

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_ori.gen_basic_test     ) ,
  asm_test( inst_ori.gen_dest_dep_test  ) ,
  asm_test( inst_ori.gen_src_dep_test   ) ,
  asm_test( inst_ori.gen_srcs_dest_test ) ,
  asm_test( inst_ori.gen_value_test     ) ,
  asm_test( inst_ori.gen_random_test    ) ,
])
def test_ori( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# xori
#-------------------------------------------------------------------------

from . import inst_xori

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_xori.gen_basic_test     ) ,
  asm_test( inst_xori.gen_dest_dep_test  ) ,
  asm_test( inst_xori.gen_src_dep_test   ) ,
  asm_test( inst_xori.gen_srcs_dest_test ) ,
  asm_test( inst_xori.gen_value_test     ) ,
  asm_test( inst_xori.gen_random_test    ) ,
])
def test_xori( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# slti
#-------------------------------------------------------------------------

from . import inst_slti

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_slti.gen_basic_test     ) ,
])
def test_slti( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# sltiu
#-------------------------------------------------------------------------

from . import inst_sltiu

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_sltiu.gen_basic_test     ) ,
])
def test_sltiu( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# srai
#-------------------------------------------------------------------------

from . import inst_srai

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_srai.gen_basic_test     ) ,
])
def test_srai( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# srli
#-------------------------------------------------------------------------

from . import inst_srli

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_srli.gen_basic_test     ) ,
])
def test_srli( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# slli
#-------------------------------------------------------------------------

from . import inst_slli

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_slli.gen_basic_test     ) ,
])
def test_slli( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# lui
#-------------------------------------------------------------------------

from . import inst_lui

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_lui.gen_basic_test    ) ,
])
def test_lui( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# auipc
#-------------------------------------------------------------------------

from . import inst_auipc

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_auipc.gen_basic_test    ) ,
])
def test_auipc( name, test ):
  run_test( ProcFL, test )

