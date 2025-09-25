#=========================================================================
# ProcFL_test.py
#=========================================================================

import pytest

from pymtl3 import *
from .harness import *
from lab2_proc.ProcFL import ProcFL

#-------------------------------------------------------------------------
# jal
#-------------------------------------------------------------------------

from . import inst_jal

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_jal.gen_basic_test        ) ,
])

def test_jal( name, test ):
  run_test( ProcFL, test )

#-------------------------------------------------------------------------
# jalr
#-------------------------------------------------------------------------

from . import inst_jalr

@pytest.mark.parametrize( "name,test", [
  asm_test( inst_jalr.gen_basic_test    ),
])

def test_jalr( name, test ):
  run_test( ProcFL, test )

