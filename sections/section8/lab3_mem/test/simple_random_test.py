#=========================================================================
# simple_test.py
#=========================================================================
# This is primarily just for playing around with little transaction
# sequences.

import pytest

from random import seed, randint

from pymtl3 import *
from pymtl3.stdlib.mem import MemoryFL, mk_mem_msg, MemMsgType
from pymtl3.stdlib.stream import StreamSourceFL, StreamSinkFL
from pymtl3.stdlib.test_utils import mk_test_case_table, run_sim

from lab3_mem.test.harness import req, resp, run_test
from lab3_mem.CacheFL      import CacheFL
from lab3_mem.CacheSimple  import CacheSimple

seed(0xa4e28cc2)

#-------------------------------------------------------------------------
# cmp_wo_test_field
#-------------------------------------------------------------------------
# The test field in the cache response is used to indicate if the
# corresponding memory access resulted in a hit or a miss. However, the
# FL model always sets the test field to zero since it does not track
# hits/misses. So we need to do something special to ignore the test
# field when using the FL model. To do this, we can pass in a specialized
# comparison function to the StreamSinkFL.

def cmp_wo_test_field( msg, ref ):

  # check type, len, and opaque fields

  if msg.type_ != ref.type_:
    return False

  if msg.len != ref.len:
    return False

  if msg.opaque != msg.opaque:
    return False

  # only check data on a read

  if ref.type_ == MemMsgType.READ:
    if ref.data != msg.data:
      return False

  # do not check the test field

  return True

#-------------------------------------------------------------------------
# Data initialization function
#-------------------------------------------------------------------------
# Function that can be used to initialize 512 bytes (128 words) of data.
# The function returns a list in this format:
#
#  [ addr0, data0, addr1, data1, addr2, data2, ... ]
#
# This list can be processed such that addr0 is initialized with data0,
# addr1 is initialized with data1, and so on.
#
# We choose data which is a direct function of the address. So the data
# stored at addr0 will be the concatentation of 0xabcd in the top 16 bits
# and the bottom 16 bits of the address. So the data at address
# 0x00001024 will be 0xabcd1024. This makes it easy to always know what
# the correct data is for any given address, but also makes sure all of
# the data is unique.

def data_1KB():
  data = []
  for i in range(256):
    data.extend([0x00001000+i*4,0xabcd1000+i*4])
  return data

#-------------------------------------------------------------------------
# Random test messages
#-------------------------------------------------------------------------

def random_msgs():

  # Create list of 100 random request messages with the corresponding
  # correct response message.

  msgs = []
  for i in range(100):

    # Choose a random index to read

    idx = randint(0,256)

    # Create address and data. Notice how we turn the random index into
    # an actual address. We multiply the index by four and then add it to
    # the base address which is 0x00001000. We can figure out the correct
    # data from the address.

    addr = 0x00001000+idx*4
    data = 0xabcd1000+idx*4

    # Create a request/response pair.

    msgs.extend([
      req( 'rd', i, addr, 0, 0 ), resp( 'rd', i, 0, 0, data ),
    ])

  return msgs

#-------------------------------------------------------------------------
# test
#-------------------------------------------------------------------------

test_case_table = mk_test_case_table([
  (                 "msg_func     mem_data_func stall lat src sink"),
  [ "random",        random_msgs, data_1KB,     0.0,  0,  0,  0    ],
  [ "random_delays", random_msgs, data_1KB,     0.9,  3,  10, 10   ],
])

@pytest.mark.parametrize( **test_case_table )
def test( test_params, cmdline_opts ):
  run_test( CacheFL(), test_params, cmdline_opts, cmp_wo_test_field )

