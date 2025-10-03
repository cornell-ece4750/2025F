//=========================================================================
// Simple Blocking Cache Datapath
//=========================================================================

`ifndef LAB3_MEM_CACHE_SIMPLE_DPATH_V
`define LAB3_MEM_CACHE_SIMPLE_DPATH_V

`include "vc/mem-msgs.v"
`include "vc/srams.v"
`include "vc/regs.v"

`include "lab3_mem/WbenDecoder.v"
`include "lab3_mem/ReplUnit.v"

module lab3_mem_CacheSimpleDpath
#(
  parameter p_num_banks = 1
)
(
  input  logic          clk,
  input  logic          reset,

  // Processor <-> Cache Interface

  input  mem_req_4B_t   proc2cache_reqstream_msg,
  output mem_resp_4B_t  proc2cache_respstream_msg,

  // Cache <-> Memory Interface

  output mem_req_16B_t  cache2mem_reqstream_msg,
  input  mem_resp_16B_t cache2mem_respstream_msg,

  // control signals (ctrl->dpath)

  input  logic          cachereq_reg_en,
  input  logic          tag_array_wen,
  input  logic          tag_array_ren,
  input  logic          data_array_wen,
  input  logic          data_array_ren,

  // status signals (dpath->ctrl)

  output logic  [2:0]   cachereq_type,
  output logic [31:0]   cachereq_addr
);

  // Register the unpacked proc2cache_reqstream_msg

  logic [31:0] cachereq_addr_reg_out;
  logic [31:0] cachereq_data_reg_out;
  logic  [2:0] cachereq_type_reg_out;
  logic  [7:0] cachereq_opaque_reg_out;

  vc_EnResetReg #(3,0) cachereq_type_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_reg_en),
    .d      (proc2cache_reqstream_msg.type_),
    .q      (cachereq_type_reg_out)
  );

  vc_EnResetReg #(32,0) cachereq_addr_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_reg_en),
    .d      (proc2cache_reqstream_msg.addr),
    .q      (cachereq_addr_reg_out)
  );

  vc_EnResetReg #(8,0) cachereq_opaque_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_reg_en),
    .d      (proc2cache_reqstream_msg.opaque),
    .q      (cachereq_opaque_reg_out)
  );

  vc_EnResetReg #(32,0) cachereq_data_reg
  (
    .clk    (clk),
    .reset  (reset),
    .en     (cachereq_reg_en),
    .d      (proc2cache_reqstream_msg.data),
    .q      (cachereq_data_reg_out)
  );

  assign cachereq_type = cachereq_type_reg_out;
  assign cachereq_addr = cachereq_addr_reg_out;

  // Address Mapping

  logic  [1:0] cachereq_addr_byte_offset;
  logic  [1:0] cachereq_addr_word_offset;
  logic  [3:0] cachereq_addr_index;
  logic [23:0] cachereq_addr_tag;

  generate
    if ( p_num_banks == 1 ) begin
      // ''' SECTION TASK ''''''''''''''''''''''''''''''''''''''''''''''''
      // Update the address map
      // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
      // assign cachereq_addr_byte_offset = cachereq_addr[??:??];
      // assign cachereq_addr_word_offset = cachereq_addr[??:??];
      // assign cachereq_addr_index       = cachereq_addr[??:??];
      // assign cachereq_addr_tag         = cachereq_addr[??:??];
    end
    else if ( p_num_banks == 4 ) begin
      // handle address mapping for four banks
    end
  endgenerate

  // Replicate cachereq_data

  logic [127:0] cachereq_data_replicated;

  lab3_mem_ReplUnit repl_unit
  (
    .in_ (cachereq_data_reg_out),
    .out (cachereq_data_replicated)
  );

  // Write byte enable decoder

  logic [15:0] wben_decoder_out;

  lab3_mem_WbenDecoder wben_decoder
  (
    .in_ (cachereq_addr_word_offset),
    .out (wben_decoder_out)
  );

  // Tag array (16 tags, 24 bits/tag)

  logic [23:0] tag_array_read_out;

  vc_CombinationalBitSRAM_1rw
  #(
    .p_data_nbits  (24),
    .p_num_entries (16)
  )
  tag_array
  (
    .clk           (clk),
    .reset         (reset),
    .read_addr     (cachereq_addr_index),
    .read_data     (tag_array_read_out),
    .write_en      (tag_array_wen),
    .read_en       (tag_array_ren),
    .write_addr    (cachereq_addr_index),
    .write_data    (cachereq_addr_tag)
  );

  // Data array (16 cacheslines, 128 bits/cacheline)

  logic [127:0] data_array_read_out;

  vc_CombinationalSRAM_1rw #(128,16) data_array
  (
    .clk           (clk),
    .reset         (reset),
    .read_addr     (cachereq_addr_index),
    .read_data     (data_array_read_out),
    .write_en      (data_array_wen),
    .read_en       (data_array_ren),
    .write_byte_en (wben_decoder_out),
    .write_addr    (cachereq_addr_index),
    .write_data    (cachereq_data_replicated)
  );

  // Hard-coded for write init response

  assign proc2cache_respstream_msg.type_  = `VC_MEM_RESP_MSG_TYPE_WRITE_INIT;
  assign proc2cache_respstream_msg.opaque = cachereq_opaque_reg_out;
  assign proc2cache_respstream_msg.test   = 2'b0;
  assign proc2cache_respstream_msg.len    = 2'b0;
  assign proc2cache_respstream_msg.data   = 32'b0;

endmodule

`endif
