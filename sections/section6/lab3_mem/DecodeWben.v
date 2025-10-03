//========================================================================
// Decoder for Write Byte Enable
//========================================================================

`ifndef LAB3_MEM_DECODER_WBEN_V
`define LAB3_MEM_DECODER_WBEN_V

//------------------------------------------------------------------------
// Decoder for Wben
//------------------------------------------------------------------------

module lab3_mem_DecoderWben
#(
  parameter p_in_nbits = 2,

  // Local constants not meant to be set from outside the module
  parameter c_out_nbits = (1 << (p_in_nbits+2))
)(
  input  logic [p_in_nbits-1:0]  in,
  output logic [c_out_nbits-1:0] out
);

  genvar i;
  generate
    for ( i = 0; i < c_out_nbits; i = i + 1 )
      begin : decode
        // Width matches only if p_in_nbits = 2
        assign out[i] = ({30'b0,in} == i/4);
      end
  endgenerate

endmodule

`endif
