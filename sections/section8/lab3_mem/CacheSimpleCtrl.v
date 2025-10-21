//=========================================================================
// Simple Blocking Cache Control
//=========================================================================

`ifndef LAB3_MEM_CACHE_SIMPLE_CTRL_V
`define LAB3_MEM_CACHE_SIMPLE_CTRL_V

`include "vc/regfiles.v"
`include "vc/mem-msgs.v"

module lab3_mem_CacheSimpleCtrl
#(
  parameter p_num_banks = 1
)
(
  input  logic        clk,
  input  logic        reset,

  // Processor <-> Cache Interface

  input  logic        proc2cache_reqstream_val,
  output logic        proc2cache_reqstream_rdy,

  output logic        proc2cache_respstream_val,
  input  logic        proc2cache_respstream_rdy,

  // Cache <-> Memory Interface

  output logic        cache2mem_reqstream_val,
  input  logic        cache2mem_reqstream_rdy,

  input  logic        cache2mem_respstream_val,
  output logic        cache2mem_respstream_rdy,

  // control signals (ctrl->dpath)

  output logic        cachereq_reg_en,
  output logic        tag_array_wen,
  output logic        tag_array_ren,
  output logic        data_array_wen,
  output logic        data_array_ren,

  // status signals (dpath->ctrl)

  input  logic  [2:0] cachereq_type,
  input  logic [31:0] cachereq_addr
);

  //----------------------------------------------------------------------
  // State Definitions
  //----------------------------------------------------------------------

  localparam STATE_IDLE             = 5'd0;
  localparam STATE_TAG_CHECK        = 5'd1;
  localparam STATE_INIT_DATA_ACCESS = 5'd2;
  localparam STATE_WAIT             = 5'd3;

  //----------------------------------------------------------------------
  // State
  //----------------------------------------------------------------------

  always @( posedge clk ) begin
    if ( reset ) begin
      state_reg <= STATE_IDLE;
    end
    else begin
      state_reg <= state_next;
    end
  end

  //----------------------------------------------------------------------
  // State Transitions
  //----------------------------------------------------------------------

  logic is_read;
  logic is_write;
  logic is_init;

  assign is_read  = cachereq_type == `VC_MEM_REQ_MSG_TYPE_READ;
  assign is_write = cachereq_type == `VC_MEM_REQ_MSG_TYPE_WRITE;
  assign is_init  = cachereq_type == `VC_MEM_REQ_MSG_TYPE_WRITE_INIT;

  logic [4:0] state_reg;
  logic [4:0] state_next;

  always @(*) begin

    state_next = state_reg;
    case ( state_reg )

      STATE_IDLE:
        if ( proc2cache_reqstream_val )
          state_next = STATE_TAG_CHECK;

      // ''' SECTION TASK ''''''''''''''''''''''''''''''''''''''''''''''''
      // Add state transitions
      // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

      STATE_TAG_CHECK:
      STATE_INIT_DATA_ACCESS:
      STATE_WAIT:

      default:
        state_next = STATE_IDLE;

    endcase

  end

  //----------------------------------------------------------------------
  // Valid/Dirty bits record
  //----------------------------------------------------------------------

  logic [3:0] cachereq_addr_index;

  generate
    if ( p_num_banks == 1 ) begin
      assign cachereq_addr_index = cachereq_addr[7:4];
    end
    else if ( p_num_banks == 4 ) begin
      // handle address mapping for four banks
    end
  endgenerate

  logic valid_bit_in;
  logic valid_bits_write_en;
  logic is_valid;

  vc_ResetRegfile_1r1w#(1,16) valid_bits
  (
    .clk        (clk),
    .reset      (reset),
    .read_addr  (cachereq_addr_index),
    .read_data  (is_valid),
    .write_en   (valid_bits_write_en),
    .write_addr (cachereq_addr_index),
    .write_data (valid_bit_in)
  );

  //----------------------------------------------------------------------
  // State Outputs
  //----------------------------------------------------------------------

  task cs
  (
    input logic cs_cachereq_rdy,
    input logic cs_cacheresp_val,
    input logic cs_cachereq_reg_en,
    input logic cs_tag_array_wen,
    input logic cs_tag_array_ren,
    input logic cs_data_array_wen,
    input logic cs_data_array_ren,
    input logic cs_valid_bit_in,
    input logic cs_valid_bits_write_en
  );
  begin
    proc2cache_reqstream_rdy  = cs_cachereq_rdy;
    proc2cache_respstream_val = cs_cacheresp_val;
    cachereq_reg_en           = cs_cachereq_reg_en;
    tag_array_wen             = cs_tag_array_wen;
    tag_array_ren             = cs_tag_array_ren;
    data_array_wen            = cs_data_array_wen;
    data_array_ren            = cs_data_array_ren;
    valid_bit_in              = cs_valid_bit_in;
    valid_bits_write_en       = cs_valid_bits_write_en;
  end
  endtask

  // Set outputs using a control signal "table"
  always @(*) begin
                              cs( 0,   0,    0,    0,    0,    0,    0,    0,    0     );
    case ( state_reg )
      //                         cache cache cache tag   tag   data  data  valid valid
      //                         req   resp  req   array array array array bit   write
      //                         rdy   val   en    wen   ren   wen   ren   in    en
      STATE_IDLE:             cs( 1,   0,    1,    0,    0,    0,    0,    0,    0     );

      // ''' SECTION  ''''''''''''''''''''''''''''''''''''''''''''''''''''
      // Add outputs for TAG_CHECK, DATA_ACCESS, WAIT states
      // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

      default:                cs( 0,   0,    0,    0,    0,    0,    0,    0,    0     );

    endcase
  end

  // Hard code cache <-> memory interface val/rdy signals since we are
  // not using this interface yet

  assign cache2mem_reqstream_val  = 1'b0;
  assign cache2mem_respstream_rdy = 1'b1;

endmodule

`endif
