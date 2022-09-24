import struct

from ..fvm import FVM, Opcode
from .code import Code, Op, OpType

class Serializer:
    """ Serializes FVM bytecode from IR code. """
    
    def get_op_size(self, op: Op) -> int:
        """ Get the compiled size of an IR operation in bytes. """
        
        if op.type == OpType.CALL_PARAMC:
            return 1 + 4 + 1
        elif op.type in (OpType.PUSH_LABEL, OpType.PUSH_INT):
            return 1 + 4
        
        return 1
    
    
    def get_labels(self, code: Code) -> dict[str, int]:
        """ Get a dictionary of label addresses from IR code. """
        
        size: int = 0
        labels: dict[str, int] = {}
        
        for block in code.blocks:
            labels[block.label] = size
            
            for op in block.ops:
                size += self.get_op_size(op)
        
        return labels
    
    
    def serialize(self, code: Code, is_flat: bool) -> bytes:
        """ Serialize FVM bytecode from IR code. """
        
        labels: dict[str, int] = self.get_labels(code)
        bytecode: bytearray = bytearray()
        
        for block in code.blocks:
            for op in block.ops:
                if op.type == OpType.HALT:
                    self.append_opcode(bytecode, Opcode.HALT)
                elif op.type == OpType.CALL_PARAMC:
                    self.append_opcode(bytecode, Opcode.PUSH_U32)
                    self.append_u32(bytecode, op.int_value)
                    self.append_opcode(bytecode, Opcode.CALL)
                elif op.type == OpType.RETURN:
                    self.append_opcode(bytecode, Opcode.RETURN)
                elif op.type == OpType.PUSH_LABEL:
                    self.append_opcode(bytecode, Opcode.PUSH_U32)
                    self.append_u32(bytecode, labels.get(op.str_value, 0))
                elif op.type == OpType.PUSH_INT:
                    self.append_opcode(bytecode, Opcode.PUSH_S32)
                    self.append_s32(bytecode, op.int_value)
                elif op.type == OpType.DISCARD:
                    self.append_opcode(bytecode, Opcode.DISCARD)
                elif op.type == OpType.PRINT:
                    self.append_opcode(bytecode, Opcode.PRINT)
                else:
                    print(f"Unimplemented IR op type '{op}'!")
                    self.append_opcode(bytecode, Opcode.NO_OPERATION)
        
        if is_flat:
            return bytes(bytecode)
        
        header: bytearray = bytearray([0] * 16)
        struct.pack_into("8s", header, 0, FVM.HEADER)
        struct.pack_into("<I", header, 8, FVM.FORMAT_VERSION)
        struct.pack_into("<I", header, 12, len(bytecode))
        return bytes(header + bytecode)
    
    
    def append_int_struct(
            self, bytecode: bytearray, format: str, size: int,
            value: int) -> None:
        """ Append an integer structure into FVM bytecode. """
        
        bytecode.extend([0] * size)
        struct.pack_into(format, bytecode, len(bytecode) - size, value)
    
    
    def append_u8(self, bytecode: bytearray, value: int) -> None:
        """ Append an 8-bit unsigned integer into FVM bytecode. """
        
        self.append_int_struct(bytecode, "B", 1, value)
    
    
    def append_u32(self, bytecode: bytearray, value: int) -> None:
        """ Append a 32-bit unsigned integer into FVM bytecode. """
        
        self.append_int_struct(bytecode, "<I", 4, value)
    
    
    def append_s32(self, bytecode: bytearray, value: int) -> None:
        """ Append a 32-bit signed integer into FVM bytecode. """
        
        self.append_int_struct(bytecode, "<i", 4, value)
    
    
    def append_opcode(self, bytecode: bytearray, opcode: Opcode) -> None:
        """ Append an FVM opcode into FVM bytecode. """
        
        self.append_u8(bytecode, opcode.value)