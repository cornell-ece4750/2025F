#=========================================================================
# crt0.S : Entry point for TinyRV2 user programs
#=========================================================================
# This file is originally grabbed from riscv-gnu-toolchain repo
#
#  - https://github.com/riscv/riscv-gnu-toolchain/blob/master/newlib/libgloss/riscv/riscv.ld
#
# According to this:
#
#  - https://github.com/riscv/riscv-gnu-toolchain/issues/42
#
# The execution environment (e.g., OS kernel) is expected to have
# initialized sp before jumping to the program's entry point. If you're
# in an embedded domain with different constraints, you need to use a
# different crt0 that sets up that kind of thing. gp is the ABI global
# pointer to the small data section. The OS doesn't initialize it because
# it's a property of the binary, not the execution environment (unlike
# the stack).
#
# This crt0.S assumes the test harness has put the command line arguments
# on the stack as illustrated below.
#
#  address
#          -------------------------------------------
#  0xffffc last word in memory
#          -------------------------------------------
#          unusedd until last argument
#          -------------------------------------------
#          arg(argc-1)  : argument argc-1
#          ...
#          arg(1)       : argument 1
#          arg(0)       : argument 0
#          -------------------------------------------
#          NULL         : extra null pointer
#          NULL         : end of argument pointers
#          argv[argc-1] : argument pointer argc-1
#          ...
#          argv[1]      : argument pointer 1
#          argv[0]      : argument pointer 0
#  0xff000 argc         : argument count                <-- stack pointer
#          -------------------------------------------
#
# Notice that we reserve a fixed size for all the argument storage. This
# is to make sure that the stack alignment is not a function of the
# arguments. Based on this layout we need to set a0 and a1 correctly as
# they are the arguments to main(). Basically argc is stored in a0 and
# equals the value pointed to by sp, and argv is stored in a1 equals
# sp+4.

  .text
  .global _start
_start:
1:
  # initialize global pointer

  auipc gp, %pcrel_hi(_gp)
  addi  gp, gp, %pcrel_lo(1b)

  # initialize stack pointer to 0xff000

  lui   sp, 0x000ff

  # allocate 0x4000 (16KB) stack memory for each core
  #  - core #0 uses 0x100000~0xfc000 as stack
  #  - core #1 uses 0xfc0000-0xf8000 as stack
  #  - core #2 uses 0xf80000-0xf4000 as stack
  #  - core #3 uses 0xf40000-0xf0000 as stack

  lui   t0, 4       # t0 = 16K
  csrr  t1, 0xf14   # t1 = tid (thread id)
  mul   t2, t0, t1  # t2 = tid * 16K
  sub   sp, sp, t2  # sp = sp - t2

  # clear the bss segment

  la    t0, _fbss   # _fbss is defined in linker script
  la    t1, _end    # _fbss is defined in linker script

1:
  sw    zero,0(t0)
  addi  t0, t0, 4
  bltu  t0, t1, 1b

  # set a0 to argc and a1 to argv

  lw    a0, 0(sp)
  addi  a1, sp, 4

  # call main

  jal   x1, main

  # use return value from main (a0) as exit code

  lui   t0, 0x10
  add   t0, t0, a0
  csrw  0x7c0, t0

  # infinite loop, should not get here

1:
  beq     zero, zero, 1b
