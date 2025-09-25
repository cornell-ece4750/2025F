
# ECE 4750 Section 5: Bug Hunt
==========================================================================

**Table of Contents**

 - Diverse Testing Strategies
 - 10-step Systematic Debugging Process

In this discussion section, we will work with a processor design that has
an injected bug. The processor implements the CSRR, CSRW, ADD, ADDI, LW,
and BNE instructions. The goal is to learn a systematic approach to
debugging by applying a robust testing strategy and following a 10-step
process to identify and resolve the bug.

Diverse Testing Strategies
--------------------------------------------------------------------------

Testing is the process of checking whether a program behaves correctly.
Testing a large design can be hard because bugs may appear anywhere in
the design, and multiple bugs may interact. Good practice is to test
small parts of the design individually, before testing the entire design,
which can more readily support finding and fixing bugs.

We will use both unit testing and integration testing. Unit testing is
the process of individually testing a small part or unit of a design,
typically a single module. A unit test is typically conducted by creating
a testbench, a.k.a. test harness, which is a separate program whose sole
purpose is to check that a module returns correct output values for a
variety of input values. Each unique set of input values is known as a
test vector. Manually examining printed output is cumbersome and error
prone. A better test harness would only print a message for incorrect
output. Integration involves testing the composition of various modules
and should only be attempted after we have unit tested those modules.

We will be using a mix of black-box and white-box testing. Black box
testing is where your test cases only test the _interface_ of your
design. Black-box testing does not _directly_ test any of the internals
within your design. Obviously, black-box testing will _indirectly_ test
the internals though. White-box testing is where your test cases directly
test the internals by perhaps poking into the design using hierarchical
signal references. White-box testing is pretty fragile so we won't really
be using it in this course. We also might do what I call "gray-box"
testing. This is where you choose specific test vectors that are
carefully designed to trigger complex behavior in a specific
implementation. Since gray-box tests can be applied to any
implementation, they are like black-box tests. Since they attempt to
trigger complex implementation-specific behavior, they are like white-box
tests.

We will primarly be using directed testing and random testing. Directed
testing is where the designer explicitly specifies the inputs and the
correct outputs. Directed tests are carefully crafted to enable good
coverage of many different hardware behaviors. Random testing is where
the designer randomly generates inputs and then verifies that the
function produces the right output. This of course begs the question,
"How do we know what the right output is, if we are randomly generating
the input?" There are two approaches. First, the designer can assert that
property is valid on the output. For example, if the module is meant to
sort a sequence of values, the random test can assert that the final
values are is indeed sorted. Second, the designer can use a golden
reference implementation. For example, the programmer might use a
functional-level model of the module.

We will also use value and delay testing. Value testing focuses on
applying different input values and checking the corresponding output
values. Delay testing focuses more on changing the delays between _when_
input values are provided and possibly also changing the delays between
_when_ output values are accepted. Delay testing is particularly
important when working with latency-insenstiive stream interfaces to
ensure the corresponding val/rdy micro-protocol is implemented correctly.
A variant of delay testing involves verifying that the delay of a module
is as expected. So for example we might assert that the module takes no
longer than a specific number of cycles to executes a specific
transaction.

Note that in practice we often mix and match different kinds of testing.
For example, we might use unit, black-box, directed, and value testing
together, or combine integration, black-box, random, and delay testing.
Keep in mind that ad-hoc testing should _not_ be a major part of your
strategy, since it is neither automatic nor systematic.

10-step Systematic Debugging Process
--------------------------------------------------------------------------

Here is our recommended systematic debugging process. Use this process
after you have fixed any Verilog syntax errors and you are now getting
some kind of incorrect result. REMEMBER: You must use `--tb=short` or
`--tb=long` to see the error message when using pytest!

**Step 1: Run all tests**

Run all of the tests to get a high-level view of which test cases are
passing and failing.

**Step 2: Zoom in on one failing test script**

Pick one failing test script to focus on, and run just that test script
in isolation with the `--verbose` flag to get a list of the test
cases. Pick the most basic test script that is failing. Always focus on
any test cases that are failing on FL model (e.g., `ProcFL`) first
since this means it is a bad test case.

**Step 3: Zoom in on one failing test case**

Pick one failing test case to focus on, and run just that test case in
isolation using `-k` (or maybe `-x`). Pick the most basic test case
that is failing. Use `-s` to see the line trace. Use `--tb=long` or
`--tb=short` to see the error message.

**Step 4: Determine the observable error**

Look at the line trace and the error message. Determine what is the
observable error. Often this will be a stream sink error but it could be
some other kind of error. Being able to crisply state the observeable
error is critical. Simply saying "my code doesn't work," or "my code
fails this test case" is not sufficient!

**Step 5: Confirm the test case is valid**

Look at the actual test case (in lab 2 this means look at the assembly
sequence). Make absolutely sure you know what the test case is testing
and that the test case is valid. You have no hope of debugging your
design if you do not understand what correct execution you expect to
happen! You might want to run the test case on FL model (e.g.,
`ProcFL`) just verify that this actually a valid test case before
continuing, although hopefully you spotted any failures on the FL model
in step 1.

**Step 6: Work backwards from observable error in line trace to
  buggy cycle**

Work _backwards_ from the observable error on the line trace trying to
see what is going wrong from just the line trace. NOTE: In lab 2, you can
see the instruction memory request and response _and_ the data memory
request and response in the line trace -- you can often spot errors for
LW or SW right from the line trace by looking at the data memory request
and response messages (incorrect message type? incorrect address?
incorrect data being read/written?). Similarly you can often spot errors
for instruction fetch from the line trace. You can also often see errors
in control flow (are the wrong instructions being executed, squashed) or
errors in stalling/bypassing logic (is an instruction not stalling when
it should?) right from the line trace. You need to work backwards from
the observable error to narrow your focus on what part of the design
might have a bug (the datapath? the control unit?). Try to narrow your
focus to a specific buggy cycle where something is going wrong.

Based on the narrowed focus from step 6, take a quick look at the
corresponding code. Check for errors in bitwidth, in signal naming, or in
connectivity. If you cannot spot anything obvious then go to the next
step. If you spot something obvious skip to step 9.

**Step 7: Zoom in on the buggy cycle in the waveform**

Use the `--dump-vcd` option to generate a VCD file. Open the VCD
file in gtkwave. Add the clock, reset, and key signals (e.g.,
`inst_D`, `inst_X`, `inst_M`, `inst_W`) to the waveform
view. Use the narrowed focus from Step 6 to zoom in on a specific cycle
and a specific part of the design where you can clearly see a specific
signal that is incorrect.

**Step 8: Work backwards in space on the buggy cycle in waveform**

Work _backwards_ from the signal which is incorrect. Work backwards in
the datapath -- keep working backwards component by component. For each
component look at the inputs (all inputs, look at data inputs and control
signals) and look at the outputs (all outputs, look at data outputs and
status signals). Check for one of three things:

 - (1) are the inputs incorrect and the outputs incorrect for this
   component? if so you need to continue working backwards -- if the
   incorrect input is a control signal then you need to start working
   backwards into the control unit;

 - (2) are the inputs correct and the outputs incorrect for this
    component? if so then you have narrowed the bug to be inside the
    component (maybe it is a bug in the ALU? maybe it is a bug in some
    other module?); or

 - (3) are the inputs correct and the outputs correct for this
    component? Then you have gone backwards too far and you need to go
    forward in again to find a signal which is incorrect.

**Step 9: Make a hypothesis on what is wrong and on buggy cycle**

Once you find a bug, make a hypothesis about what should happen if you
fix the bug. Your hypothesis should not just be "fixing the bug will make
the test pass." It should instead be something like "fixing this bug
should make this specific signal be 1 instead of 0" or "fixing this bug
should make this specific instruction in the line trace stall".

**Step 10: Fix bug and test hypothesis**

Fix the bug and see what happens by looking at the line trace and/or
waveform. Don't just see if it passes the test -- literally check the
line trace and/or waveform and see if the behavior confirms the line
trace. One of four things will happen:

 - (1) the test will pass and the linetrace/waveform behavior will
    match your hypothesis -- bug fixed!

 - (2) the test will fail and the linetrace/waveform will not match
    your hypothesis -- you need to keep working -- your bug fix did not
    do what it was supposed to, and it did not fix the error -- undo the
    bug fix and go back to step 6.

 - (3) the test will fail but the linetrace/waveform _will_ match
    your hypothesis -- this means your bug fix did what you expected but
    there might be another bug still causing trouble -- you need to keep
    working -- go back to step 6.

 - (4) the test will pass and the linetrace/waveform _will not_
    match your hypothesis -- you need to keep working -- your bug fix did
    not do what you thought it would even though it cause the test to
    pass -- there might be something subtle going on -- go back to step 6
    to figure out why the bug fix did not do what you thought it would.

Note a couple things about this systematic 10 step process. First, it is
a systematic process ... it does not involve randomly trying things.
Second, the process uses all tools at your disposable: output from
pytest, traceback, line tracing, and VCD waveforms. You really need to
use all of these tools. If you use line tracing but never use VCD
waveforms or you use VCD waveforms and never use line tracing then you
are putting yourself at a disadvantage. Third, the process requires you
to think critically and make a hypothesis about what should change -- do
not just change something, pass the test, and move on -- change something
and see if the line trace and waveforms change in the way you expect.
Otherwise you can actually introduce more bugs even though you think are
fixing things.
