//========================================================================
// NormalQueue with one entry
//========================================================================

`ifndef SEC08_QUEUES_NORMAL_QUEUE_1_V
`define SEC08_QUEUES_NORMAL_QUEUE_1_V

`include "vc/queues.v"

module sec08_queues_NormalQueue1
(
  input  logic        clk,
  input  logic        reset,

  input  logic        istream_val,
  output logic        istream_rdy,
  input  logic [31:0] istream_msg,

  output logic        ostream_val,
  input  logic        ostream_rdy,
  output logic [31:0] ostream_msg
);

  logic num_free_entries;

  vc_Queue
  #(
    .p_type      (`VC_QUEUE_NORMAL),
    .p_msg_nbits (32),
    .p_num_msgs  (1)
  )
  queue
  (
    .clk     (clk),
    .reset   (reset),

    .enq_val (istream_val),
    .enq_rdy (istream_rdy),
    .enq_msg (istream_msg),

    .deq_val (ostream_val),
    .deq_rdy (ostream_rdy),
    .deq_msg (ostream_msg),

    .num_free_entries (num_free_entries)
  );

endmodule

`endif
