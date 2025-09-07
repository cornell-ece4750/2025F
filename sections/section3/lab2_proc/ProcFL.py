"""
==========================================================================
ProcFL
==========================================================================
TinyRV2 FL processor

Author : Shunning Jiang, Peitian Pan, Christopher Batten
  Date : Sep 12, 2022
"""

from pymtl3 import *
from pymtl3.extra import clone_deepcopy
from pymtl3.stdlib.stream.ifcs import IStreamIfc, OStreamIfc
from pymtl3.stdlib.stream      import IStreamDeqAdapterFL, OStreamEnqAdapterFL
from pymtl3.stdlib.mem.ifcs    import MemRequesterIfc
from pymtl3.stdlib.mem         import mk_mem_msg, MemRequesterAdapterFL

from .tinyrv2_encoding import TinyRV2Inst, disassemble_inst

class RegisterFile(object):

  def __init__( self, nregs ):
    self.regs = [ b32(0) for i in range(nregs) ]

  def __getitem__( self, idx ):
    return self.regs[idx]

  def __setitem__( self, idx, value ):
    if idx != 0:
      self.regs[idx] = Bits32( int(value), trunc_int=True )

class ProcFL( Component ):

  def construct( s, num_cores=1 ):

    # Interface

    req_class, resp_class = mk_mem_msg( 8, 32, 32 )

    s.proc2mngr   = OStreamIfc( Bits32 )
    s.mngr2proc   = IStreamIfc( Bits32 )

    s.imem        = MemRequesterIfc( req_class, resp_class )
    s.dmem        = MemRequesterIfc( req_class, resp_class )

    s.core_id     = InPort(32)
    s.commit_inst = OutPort()
    s.stats_en    = OutPort()

    # Adapters

    s.proc2mngr_q = OStreamEnqAdapterFL( Bits32 )
    s.mngr2proc_q = IStreamDeqAdapterFL( Bits32 )

    connect( s.mngr2proc, s.mngr2proc_q.istream )
    connect( s.proc2mngr_q.ostream, s.proc2mngr )

    s.imem_adapter = MemRequesterAdapterFL( req_class, resp_class )
    s.dmem_adapter = MemRequesterAdapterFL( req_class, resp_class )

    connect( s.imem, s.imem_adapter.requester )
    connect( s.dmem, s.dmem_adapter.requester )

    # Internal data structures

    s.PC = b32( 0x200 )

    s.R = RegisterFile(32)
    s.raw_inst = None

    @update_once
    def up_ProcFL():
      if s.reset:
        s.PC = b32( 0x200 )
        return

      s.commit_inst @= 0

      try:
        s.raw_inst = s.imem_adapter.read( s.PC, 4 ) # line trace

        inst = TinyRV2Inst( s.raw_inst )
        inst_name = inst.name

        if   inst_name == "nop":
          s.PC += 4
        elif inst_name == "add":
          s.R[inst.rd] = s.R[inst.rs1] + s.R[inst.rs2]
          s.PC += 4
        elif inst_name == "sub":
          s.R[inst.rd] = s.R[inst.rs1] - s.R[inst.rs2]
          s.PC += 4
        elif inst_name == "sll":
          s.R[inst.rd] = s.R[inst.rs1] << (s.R[inst.rs2].uint() & 0x1F)
          s.PC += 4
        elif inst_name == "slt":
          s.R[inst.rd] = s.R[inst.rs1].int() < s.R[inst.rs2].int()
          s.PC += 4
        elif inst_name == "sltu":
          s.R[inst.rd] = s.R[inst.rs1] < s.R[inst.rs2]
          s.PC += 4
        elif inst_name == "xor":
          s.R[inst.rd] = s.R[inst.rs1] ^ s.R[inst.rs2]
          s.PC += 4
        elif inst_name == "srl":
          s.R[inst.rd] = s.R[inst.rs1] >> (s.R[inst.rs2].uint() & 0x1F)
          s.PC += 4
        elif inst_name == "sra":
          s.R[inst.rd] = s.R[inst.rs1].int() >> (s.R[inst.rs2].uint() & 0x1F) # sra
          s.PC += 4
        elif inst_name == "or":
          s.R[inst.rd] = s.R[inst.rs1] | s.R[inst.rs2]
          s.PC += 4
        elif inst_name == "and":
          s.R[inst.rd] = s.R[inst.rs1] & s.R[inst.rs2]
          s.PC += 4
        elif inst_name == "mul":
          s.R[inst.rd] = s.R[inst.rs1] * s.R[inst.rs2]
          s.PC += 4

        elif inst_name == "addi":
          s.R[inst.rd] = s.R[inst.rs1] + sext( inst.i_imm, 32 )
          s.PC += 4
        elif inst_name == "slti":
          s.R[inst.rd] = s.R[inst.rs1].int() < inst.i_imm.int()
          s.PC += 4
        elif inst_name == "sltiu":
          s.R[inst.rd] = s.R[inst.rs1] < sext( inst.i_imm, 32 )
          s.PC += 4
        elif inst_name == "xori":
          s.R[inst.rd] = s.R[inst.rs1] ^ sext( inst.i_imm, 32 )
          s.PC += 4
        elif inst_name == "ori":
          s.R[inst.rd] = s.R[inst.rs1] | sext( inst.i_imm, 32 )
          s.PC += 4
        elif inst_name == "andi":
          s.R[inst.rd] = s.R[inst.rs1] & sext( inst.i_imm, 32 )
          s.PC += 4
        elif inst_name == "slli":
          s.R[inst.rd] = s.R[inst.rs1] << inst.shamt.uint()
          s.PC += 4
        elif inst_name == "srli":
          s.R[inst.rd] = s.R[inst.rs1] >> inst.shamt.uint()
          s.PC += 4
        elif inst_name == "srai":
          s.R[inst.rd] = Bits32( s.R[inst.rs1].int() >> inst.shamt.uint() )
          s.PC += 4

        elif inst_name == "lui":
          s.R[inst.rd] = inst.u_imm
          s.PC += 4
        elif inst_name == "auipc":
          s.R[inst.rd] = inst.u_imm + s.PC
          s.PC += 4

        elif inst_name == "lw":
          addr = s.R[inst.rs1] + sext( inst.i_imm, 32 )
          s.R[inst.rd] = s.dmem_adapter.read( addr, 4 )
          s.PC += 4
        elif inst_name == "sw":
          addr = s.R[inst.rs1] + sext( inst.s_imm, 32 )
          s.dmem_adapter.write( addr, 4, s.R[inst.rs2] )
          s.PC += 4

        elif inst_name == "bne":
          if s.R[inst.rs1] != s.R[inst.rs2]:
            s.PC = s.PC + sext( inst.b_imm, 32 )
          else:
            s.PC += 4
        elif inst_name == "beq":
          if s.R[inst.rs1] == s.R[inst.rs2]:
            s.PC = s.PC + sext( inst.b_imm, 32 )
          else:
            s.PC += 4
        elif inst_name == "blt":
          if s.R[inst.rs1].int() < s.R[inst.rs2].int():
            s.PC = s.PC + sext( inst.b_imm, 32 )
          else:
            s.PC += 4
        elif inst_name == "bge":
          if s.R[inst.rs1].int() >= s.R[inst.rs2].int():
            s.PC = s.PC + sext( inst.b_imm, 32 )
          else:
            s.PC += 4
        elif inst_name == "bltu":
          if s.R[inst.rs1] < s.R[inst.rs2]:
            s.PC = s.PC + sext( inst.b_imm, 32 )
          else:
            s.PC += 4
        elif inst_name == "bgeu":
          if s.R[inst.rs1] >= s.R[inst.rs2]:
            s.PC = s.PC + sext( inst.b_imm, 32 )
          else:
            s.PC += 4

        elif inst_name == "jal":
          s.R[inst.rd] = s.PC + 4
          s.PC = s.PC + sext( inst.j_imm, 32 )

        elif inst_name == "jalr":
          temp = s.R[inst.rs1] + sext( inst.i_imm, 32 )
          s.R[inst.rd] = s.PC + 4
          s.PC = temp & 0xFFFFFFFE

        elif inst_name == "csrw":
          if   inst.csrnum == 0x7C0:
            if not s.proc2mngr_q.enq.rdy():
              return
            s.proc2mngr_q.enq( s.R[inst.rs1] )
          elif inst.csrnum == 0x7C1:
            s.stats_en @= trunc(s.R[inst.rs1],1)
          else:
            raise TinyRV2Semantics.IllegalInstruction(
              "Unrecognized CSR register ({}) for csrw at PC={}" \
                .format(inst.csrnum.uint(),s.PC) )
          s.PC += 4

        elif inst_name == "csrr":
          if   inst.csrnum == 0xFC0:
            if not s.mngr2proc_q.deq.rdy():
              return
            s.R[inst.rd] = s.mngr2proc_q.deq()
          elif inst.csrnum == 0xFC1:
            s.R[inst.rd] = num_cores
          elif inst.csrnum == 0xF14:
            s.R[inst.rd] = s.core_id
          else:
            raise TinyRV2Semantics.IllegalInstruction(
              "Unrecognized CSR register ({}) for csrr at PC={}" \
                .format(inst.csrnum.uint(),s.PC) )
          s.PC += 4

      except:
        print( "Unexpected error at PC={:0>8s}!".format( str(s.PC) ) )
        raise

      s.commit_inst @= 1

  #-----------------------------------------------------------------------
  # line_trace
  #-----------------------------------------------------------------------

  def line_trace( s ):
    if s.commit_inst:
      return "{:0>8s} {: <24}".format( str(s.PC), disassemble_inst( s.raw_inst ) )
    return "{}".format( "#".ljust(33) )

