#=========================================================================
# ProcSimple_test.py
#=========================================================================

import pytest
import random

from pymtl3 import *
from .harness import *
from lab2_proc.ProcSimple import ProcSimple

#-------------------------------------------------------------------------
# csr
#-------------------------------------------------------------------------

from . import inst_csr

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_csr.gen_basic_test      ),
  asm_test( inst_csr.gen_bypass_test     ),
  asm_test( inst_csr.gen_value_test      ),
  asm_test( inst_csr.gen_random_test     ),
  asm_test( inst_csr.gen_core_stats_test ),
])
def test_csr( name, test, cmdline_opts ):
  run_test( ProcSimple, test, cmdline_opts=cmdline_opts )

def test_csr_rand_delays( cmdline_opts ):
  run_test( ProcSimple, inst_csr.gen_random_test,
            src_delay=3, sink_delay=10, mem_stall_prob=0.5, mem_latency=3,
            cmdline_opts=cmdline_opts )

#-------------------------------------------------------------------------
# add
#-------------------------------------------------------------------------

from . import inst_add

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_add.gen_basic_test     ),
  asm_test( inst_add.gen_dest_dep_test  ),
  asm_test( inst_add.gen_src0_dep_test  ),
  asm_test( inst_add.gen_src1_dep_test  ),
  asm_test( inst_add.gen_srcs_dep_test  ),
  asm_test( inst_add.gen_srcs_dest_test ),
  asm_test( inst_add.gen_value_test     ),
  asm_test( inst_add.gen_random_test    ),
])
def test_add( name, test, cmdline_opts ):
  run_test( ProcSimple, test, cmdline_opts=cmdline_opts )

def test_add_rand_delays( cmdline_opts ):
  run_test( ProcSimple, inst_add.gen_random_test,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3,
            cmdline_opts=cmdline_opts )

#-------------------------------------------------------------------------
# addi
#-------------------------------------------------------------------------

from . import inst_addi

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_addi.gen_basic_test     ),
  asm_test( inst_addi.gen_dest_dep_test  ),
  asm_test( inst_addi.gen_src_dep_test   ),
  asm_test( inst_addi.gen_srcs_dest_test ),
  asm_test( inst_addi.gen_value_test     ),
  asm_test( inst_addi.gen_random_test    ),
])
def test_addi( name, test, cmdline_opts ):
  run_test( ProcSimple, test, cmdline_opts=cmdline_opts )

def test_addi_rand_delays( cmdline_opts ):
  run_test( ProcSimple, inst_addi.gen_random_test,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3,
            cmdline_opts=cmdline_opts )

#-------------------------------------------------------------------------
# lw
#-------------------------------------------------------------------------

from . import inst_lw

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_lw.gen_basic_test     ),
  asm_test( inst_lw.gen_dest_dep_test  ),
  asm_test( inst_lw.gen_base_dep_test  ),
  asm_test( inst_lw.gen_srcs_dest_test ),
  asm_test( inst_lw.gen_addr_test     ),
  asm_test( inst_lw.gen_random_test    ),
])
def test_lw( name, test, cmdline_opts ):
  run_test( ProcSimple, test, cmdline_opts=cmdline_opts )

def test_lw_rand_delays( cmdline_opts ):
  run_test( ProcSimple, inst_lw.gen_random_test,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3,
            cmdline_opts=cmdline_opts )

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
def test_bne( name, test, cmdline_opts ):
  run_test( ProcSimple, test, cmdline_opts=cmdline_opts )

def test_bne_rand_delays( cmdline_opts ):
  run_test( ProcSimple, inst_bne.gen_random_test,
            src_delay=3, sink_delay=5, mem_stall_prob=0.5, mem_latency=3,
            cmdline_opts=cmdline_opts )

