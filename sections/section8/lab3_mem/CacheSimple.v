//=========================================================================
// Simple Blocking Cache
//=========================================================================
// This simple cache only supports the write init transaction. It is
// meant as a possible starting point for lab 3.

`ifndef LAB3_MEM_CACHE_SIMPLE_V
`define LAB3_MEM_CACHE_SIMPLE_V

`include "vc/mem-msgs.v"
`include "vc/trace.v"

`include "lab3_mem/CacheSimpleCtrl.v"
`include "lab3_mem/CacheSimpleDpath.v"

module lab3_mem_CacheSimple
#(
  parameter p_num_banks = 1 // Total number of cache banks
)
(
  input  logic          clk,
  input  logic          reset,

  // Processor <-> Cache Interface

  input  mem_req_4B_t   proc2cache_reqstream_msg,
  input  logic          proc2cache_reqstream_val,
  output logic          proc2cache_reqstream_rdy,

  output mem_resp_4B_t  proc2cache_respstream_msg,
  output logic          proc2cache_respstream_val,
  input  logic          proc2cache_respstream_rdy,

  // Cache <-> Memory Interface

  output mem_req_16B_t  cache2mem_reqstream_msg,
  output logic          cache2mem_reqstream_val,
  input  logic          cache2mem_reqstream_rdy,

  input  mem_resp_16B_t cache2mem_respstream_msg,
  input  logic          cache2mem_respstream_val,
  output logic          cache2mem_respstream_rdy
);

  //----------------------------------------------------------------------
  // Wires
  //----------------------------------------------------------------------

  // control signals (ctrl->dpath)

  logic        cachereq_reg_en;
  logic        tag_array_wen;
  logic        tag_array_ren;
  logic        data_array_wen;
  logic        data_array_ren;

  // status signals (dpath->ctrl)

  logic [ 2:0] cachereq_type;
  logic [31:0] cachereq_addr;

  //----------------------------------------------------------------------
  // Control
  //----------------------------------------------------------------------

  lab3_mem_CacheSimpleCtrl
  #(
    .p_num_banks              (p_num_banks)
  )
  ctrl
  (
   // Processor <-> Cache Interface

   .proc2cache_reqstream_val  (proc2cache_reqstream_val),
   .proc2cache_reqstream_rdy  (proc2cache_reqstream_rdy),
   .proc2cache_respstream_val (proc2cache_respstream_val),
   .proc2cache_respstream_rdy (proc2cache_respstream_rdy),

   // Cache <-> Memory Interface

   .cache2mem_reqstream_val   (cache2mem_reqstream_val),
   .cache2mem_reqstream_rdy   (cache2mem_reqstream_rdy),
   .cache2mem_respstream_val  (cache2mem_respstream_val),
   .cache2mem_respstream_rdy  (cache2mem_respstream_rdy),

    // clk/reset/control/status signals

   .*
  );

  //----------------------------------------------------------------------
  // Datapath
  //----------------------------------------------------------------------

  lab3_mem_CacheSimpleDpath
  #(
    .p_num_banks              (p_num_banks)
  )
  dpath
  (
   // Processor <-> Cache Interface

   .proc2cache_reqstream_msg  (proc2cache_reqstream_msg),
   .proc2cache_respstream_msg (proc2cache_respstream_msg),

   // Cache <-> Memory Interface

   .cache2mem_reqstream_msg   (cache2mem_reqstream_msg),
   .cache2mem_respstream_msg  (cache2mem_respstream_msg),

    // clk/reset/control/status signals

   .*
  );

  //----------------------------------------------------------------------
  // Line tracing
  //----------------------------------------------------------------------

  `ifndef SYNTHESIS

  integer i;

  logic [`VC_TRACE_NBITS-1:0] str;
  `VC_TRACE_BEGIN
  begin

    vc_trace.append_str( trace_str, "(" );

    // Display state

    case ( ctrl.state_reg )

      ctrl.STATE_IDLE:             vc_trace.append_str( trace_str, "I " );
      ctrl.STATE_TAG_CHECK:        vc_trace.append_str( trace_str, "TC" );
      ctrl.STATE_INIT_DATA_ACCESS: vc_trace.append_str( trace_str, "IN" );
      ctrl.STATE_WAIT:             vc_trace.append_str( trace_str, "W " );
      default:                     vc_trace.append_str( trace_str, "? " );

    endcase

    // Display all tags

    vc_trace.append_str( trace_str, "[" );
    for ( i = 0; i < 16; i = i + 1 ) begin
      if ( !ctrl.valid_bits.rfile[i] )
        vc_trace.append_str( trace_str, " - " );
      else begin
        $sformat( str, "%x", dpath.tag_array.mem[i][11:0] );
        vc_trace.append_str( trace_str, str );
      end
      if ( i != 15 )
        vc_trace.append_str( trace_str, "|" );
    end
    vc_trace.append_str( trace_str, "]" );

    vc_trace.append_str( trace_str, ")" );

  end
  `VC_TRACE_END

  `endif

endmodule

`endif
