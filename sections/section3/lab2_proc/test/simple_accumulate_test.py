#=========================================================================
# simple_accumulate_test.py
#=========================================================================

import pytest
import random

from pymtl3 import *
from .harness import *
from lab2_proc.ProcFL import ProcFL
from lab2_proc.ProcSimple import ProcSimple

def test_accumulate( cmdline_opts ):

  prog="""
    # initialize base address and size of array
    csrr x11, mngr2proc < 0x00002000 # base address
    csrr x12, mngr2proc < 8          # size

    # write your assembly implementation of the accumulate function here!



    # put the final result in x10 so the following instruction can send
    # this result to be checked by the stream sink

    csrw proc2mngr, x10 > 54

    .data
    .word  1
    .word  1
    .word  2
    .word  3
    .word  5
    .word  8
    .word 13
    .word 21
  """

  run_test( ProcFL, prog, cmdline_opts=cmdline_opts )

