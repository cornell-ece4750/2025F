//========================================================================
// Repl Unit
//========================================================================
// Simple unit that takes as input a 32-bit input replicates it four
// times to produces a 128-bit output.

`ifndef LAB3_MEM_REPL_UNIT_V
`define LAB3_MEM_REPL_UNIT_V

module lab3_mem_ReplUnit
(
  input  logic [ 31:0] in_,
  output logic [127:0] out
);

  assign out[  31:0] = in_;
  assign out[ 63:32] = in_;
  assign out[ 95:64] = in_;
  assign out[127:96] = in_;

endmodule

`endif
