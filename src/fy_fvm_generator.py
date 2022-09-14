import struct

from fvm import FVM
from fvm_opcode import Opcode
from fy_ir_code import IRCode
from fy_ir_op_type import IROpType

class FVMGenerator:
    """ Generates FVM bytecode from IR code. """
    
    def generate(self, code: IRCode, is_flat: bool) -> bytes:
        """ Generate FVM bytecode from IR code. """
        
        labels: dict[str, int] = self.collect_labels(code)
        bytecode: bytearray = bytearray([0] * 16)
        
        for block in code.blocks:
            for op in block.ops:
                if op.type == IROpType.HALT:
                    self.insert_opcode(bytecode, Opcode.HALT)
                elif op.type == IROpType.NO_OPERATION:
                    self.insert_opcode(bytecode, Opcode.NO_OPERATION)
                elif op.type == IROpType.BRANCH_ALWAYS_LABEL:
                    self.insert_opcode(bytecode, Opcode.PUSH_U32)
                    self.insert_u32(bytecode, labels.get(op.str_value, 0))
                    self.insert_opcode(bytecode, Opcode.BRANCH_ALWAYS)
                elif op.type == IROpType.CALL_ARGC:
                    self.insert_opcode(bytecode, Opcode.PUSH_U32)
                    self.insert_u32(bytecode, op.int_value)
                    self.insert_opcode(bytecode, Opcode.CALL)
                elif op.type == IROpType.RETURN:
                    self.insert_opcode(bytecode, Opcode.RETURN)
                elif op.type == IROpType.PUSH_LABEL:
                    self.insert_opcode(bytecode, Opcode.PUSH_U32)
                    self.insert_u32(bytecode, labels.get(op.str_value, 0))
                elif op.type == IROpType.PUSH_INT:
                    self.insert_opcode(bytecode, Opcode.PUSH_S32)
                    self.insert_s32(bytecode, op.int_value)
                elif op.type == IROpType.DISCARD:
                    self.insert_opcode(bytecode, Opcode.DISCARD)
                elif op.type == IROpType.PRINT:
                    self.insert_opcode(bytecode, Opcode.PRINT)
                else:
                    print(f"Bytecode generator bug: Unimplemented IR operation '{op}'!")
        
        if is_flat:
            return bytes(bytecode[16:len(bytecode)])
        else:
            fvm: FVM = FVM()
            struct.pack_into("8s", bytecode, 0, fvm.HEADER)
            struct.pack_into("<I", bytecode, 8, fvm.FORMAT_VERSION)
            struct.pack_into("<I", bytecode, 12, len(bytecode) - 16)
            return bytes(bytecode)
    
    
    def collect_labels(self, code: IRCode) -> dict[str, int]:
        """ Collect a dictionary of label addresses from IR code. """
        
        size: int = 0
        labels: dict[str, int] = {}
        
        for block in code.blocks:
            labels[block.label] = size
            
            for op in block.ops:
                size += op.get_size()
        
        return labels
    
    
    def insert_u8(self, bytecode: bytearray, value: int) -> None:
        """ Insert an 8-bit unsigned integer into FVM bytecode. """
        
        bytecode.append(0)
        struct.pack_into("B", bytecode, len(bytecode) - 1, value)
    
    
    def insert_u32(self, bytecode: bytearray, value: int) -> None:
        """ Insert a 32-bit unsigned integer into FVM bytecode. """
        
        bytecode.extend([0] * 4)
        struct.pack_into("<I", bytecode, len(bytecode) - 4, value)
    
    
    def insert_s32(self, bytecode: bytearray, value: int) -> None:
        """ Insert a 32-bit signed integer into FVM bytecode. """
        
        bytecode.extend([0] * 4)
        struct.pack_into("<i", bytecode, len(bytecode) - 4, value)
    
    
    def insert_opcode(self, bytecode: bytearray, opcode: Opcode) -> None:
        """ Insert an FVM opcode into FVM bytecode. """
        
        self.insert_u8(bytecode, opcode.value)
