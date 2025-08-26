
Cross-compile a simple C program for RISC-V RV32IM
==========================================================================


**Table of Contents**

 - Compile a simple C program for Intel x86
 - Cross-compile a simple C program for RISC-V RV32IM


### Compile a simple C program for Intel x86

Let's compile the very first program you saw in ECE 2400. First make sure
we have a directory to work in:

    % mkdir -p ${HOME}/ece4750/2025F/helpful/cross_compile
    % cd ${HOME}/ece4750/2025F/cross_compile

Then use your favorite text editor to create a file named `avg-main.c`.

    #include <stdio.h>

    int avg( int x, int y )
    {
      int sum = x + y;
      return sum / 2;
    }

    int main()
    {
      int a = 10;
      int b = 20;
      int c = avg( a, b );
      printf( "average of %d and %d is %d\n", a, b, c );
      return  0;
    }

Recall how to compile this C program into an x86 binary and execute this
binary on the `ecelinux` server.

    % cd ${HOME}/ece4750/2025F/helpful/cross_compile
    % gcc -Wall -o avg-main avg-main.c
    % ./avg-main

### Cross-compile a simple C program for RISC-V RV32IM

In this course, we will be using the RISC-V instruction set architecture
instead of the x86 instruction set architecture. You can use a
_cross-compiler_ to compile a C program into a RISC-V binary like this:

    % cd ${HOME}/ece4750/2025F/helpful/cross_compile
    % riscv32-unknown-elf-gcc -O3 -o avg-main-riscv avg-main.c

Now let's take a look at the actual RISCV instructions using
`riscv32-objdump`:

    % riscv32-objdump avg-main-riscv

See if you can find the instructions that correspond to the `avg`
function. See if you can figure out how the C code maps to these RISCV
instructions. Use the TinyRV2 instruction set architecture manual located
here:

 - <https://www.csl.cornell.edu/courses/ece4750/handouts/ece4750-tinyrv-isa.txt>

Experiment with the following variation and look at the corresponding
RISCV instructions.

    unsigned int avg( unsigned int x, unsigned int y )
    {
      unsigned int sum = x + y;
      return sum / 2;
    }

Can you explain the difference from the original version of this code?

### Execute RISC-V instructions on a simulator

CS 3410 uses a neat RISC-V simulator which works in your browser:

 - <https://www.cs.cornell.edu/courses/cs3410/2019sp/riscv/interpreter>

Try copying the RISC-V instructions for just the `avg` function into this
RISC-V interpreter. Then execute instruction step-by-step and verify they
behave as expected.


