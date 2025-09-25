#=========================================================================
# simple_add_test.py
#=========================================================================

import pytest
import random

from pymtl3 import *
from .harness import *
from lab2_proc.ProcFL import ProcFL
from lab2_proc.ProcSimple import ProcSimple

#-------------------------------------------------------------------------
# test_add_sm
#-------------------------------------------------------------------------

def test_add_sm( cmdline_opts ):

  prog="""
    csrr x1, mngr2proc < 5
    csrr x2, mngr2proc < 4
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    add x3, x1, x2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 9
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

  run_test( ProcFL, prog, cmdline_opts=cmdline_opts )

