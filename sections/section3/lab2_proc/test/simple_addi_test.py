#=========================================================================
# simple_addi_test.py
#=========================================================================

import pytest
import random

from pymtl3 import *
from .harness import *
from lab2_proc.ProcFL import ProcFL
from lab2_proc.ProcSimple import ProcSimple

#-------------------------------------------------------------------------
# test_addi
#-------------------------------------------------------------------------

def test_addi( cmdline_opts ):

  prog="""
    # write your test case here!


  """

  run_test( ProcFL, prog, cmdline_opts=cmdline_opts )

