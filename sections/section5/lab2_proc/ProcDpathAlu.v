//========================================================================
// Proc Datapath ALU
//========================================================================

`ifndef LAB2_PROC_PROC_DPATH_ALU_V
`define LAB2_PROC_PROC_DPATH_ALU_V

`include "vc/arithmetic.v"

module lab2_proc_ProcDpathAlu
(
  input  logic [31:0] in0,
  input  logic [31:0] in1,
  input  logic [ 3:0] fn,
  output logic [31:0] out,
  output logic        ops_eq,
  output logic        ops_lt,
  output logic        ops_ltu
);

  always_comb begin

    case ( fn )
      4'd0    : out = in0 + in1;                                // ADD
      4'd11   : out = in0;                                      // CP OP0
      4'd12   : out = in1;                                      // CP OP1
      default : out = 32'b0;
    endcase

  end

  // Calculate equality, zero, negative flags

  vc_EqComparator #(32) cond_eq_comp
  (
    .in0  (in0),
    .in1  (in1),
    .out  (ops_eq)
  );

  assign ops_lt = $signed(in0) < $signed(in1);
  assign ops_ltu = in0 < in1;

endmodule

`endif /* LAB2_PROC_PROC_DPATH_ALU_V */

