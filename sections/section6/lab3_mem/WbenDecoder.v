//========================================================================
// Write Byte Enable Decoder
//========================================================================
// Simple decoder that takes as input a 2-bit binary input which
// indicates the word we want to write. The output is a 16-bit value
// where a one means to write the corresponding byte.

`ifndef LAB3_MEM_WBEN_DECODER_V
`define LAB3_MEM_WBEN_DECODER_V

module lab3_mem_WbenDecoder
(
  input  logic  [1:0] in_,
  output logic [15:0] out
);

  always_comb begin
    case ( in_ )
      2'd0: out = 16'h000f;
      2'd1: out = 16'h00f0;
      2'd2: out = 16'h0f00;
      2'd3: out = 16'hf000;
    endcase
  end

endmodule

`endif
