import struct

from ..fvm import FVM, Opcode
from .code import Code, Op, OpType

class Serializer:
    """ Serializes FVM bytecode from IR code. """
    
    FRAME_HEADER_SIZE: int = 2
    """ The size of a stack frame header in words. """
    
    def get_op_size(self, op: Op) -> int:
        """ Get the compiled size of an IR operation in bytes. """
        
        if op.type in (
                OpType.JUMP_LABEL, OpType.JUMP_NOT_ZERO_LABEL,
                OpType.JUMP_ZERO_LABEL, OpType.CALL_PARAMC,
                OpType.LOAD_LOCAL_OFFSET, OpType.STORE_LOCAL_OFFSET):
            return 1 + 4 + 1
        elif op.type in (OpType.PUSH_LABEL, OpType.PUSH_INT, OpType.PUSH_STR):
            return 1 + 4
        elif op.type == OpType.PUSH_CHR:
            return 1 + 1
        
        return 1
    
    
    def get_labels(self, code: Code) -> dict[str, int]:
        """ Get a dictionary of label addresses from IR code. """
        
        size: int = 0
        labels: dict[str, int] = {}
        
        for block in code.blocks:
            labels[block.label] = size
            
            for op in block.ops:
                size += self.get_op_size(op)
        
        labels[".end"] = size
        return labels
    
    
    def get_string_table(self, code: Code) -> list[str]:
        """ Get a string table from IR code. """
        
        # Sort strings by length.
        sorted_strings: list[str] = []
        
        for block in code.blocks:
            for op in block.ops:
                if op.type == OpType.PUSH_STR:
                    index: int = len(sorted_strings)
                    
                    while index > 0:
                        previous: str = sorted_strings[index - 1]
                        
                        if len(op.str_value) <= len(previous):
                            break
                        
                        index -= 1
                    
                    sorted_strings.insert(index, op.str_value)
        
        string_table: list[str] = []
        
        for string in sorted_strings:
            has_found_string: bool = False
            
            for i in range(len(string_table)):
                if string_table[i].endswith(string):
                    has_found_string = True
                    break
                elif string.endswith(string_table[i]):
                    string_table[i] = string
                    has_found_string = True
                    break
            
            if not has_found_string:
                string_table.append(string)
        
        return string_table
    
    
    def get_string_offset(self, string: str, string_table: list[str]) -> int:
        """ Get a string's offset into a string table. """
        
        offset: int = 0
        
        for table_string in string_table:
            if table_string.endswith(string):
                return len(table_string) - len(string) + offset
            
            offset += len(table_string) + 1
        
        return 0
    
    
    def serialize(self, code: Code, is_flat: bool) -> bytes:
        """ Serialize FVM bytecode from IR code. """
        
        labels: dict[str, int] = self.get_labels(code)
        strings: list[str] = self.get_string_table(code)
        strings_pos: int = labels.get(".end", 0)
        bytecode: bytearray = bytearray()
        
        for block in code.blocks:
            for op in block.ops:
                if op.type == OpType.HALT:
                    self.append_opcode(bytecode, Opcode.HALT)
                elif op.type == OpType.JUMP_LABEL:
                    self.append_opcode(bytecode, Opcode.PUSH_U32)
                    self.append_u32(bytecode, labels.get(op.str_value, 0))
                    self.append_opcode(bytecode, Opcode.JUMP)
                elif op.type == OpType.JUMP_NOT_ZERO_LABEL:
                    self.append_opcode(bytecode, Opcode.PUSH_U32)
                    self.append_u32(bytecode, labels.get(op.str_value, 0))
                    self.append_opcode(bytecode, Opcode.JUMP_NOT_ZERO)
                elif op.type == OpType.JUMP_ZERO_LABEL:
                    self.append_opcode(bytecode, Opcode.PUSH_U32)
                    self.append_u32(bytecode, labels.get(op.str_value, 0))
                    self.append_opcode(bytecode, Opcode.JUMP_ZERO)
                elif op.type == OpType.CALL_PARAMC:
                    self.append_opcode(bytecode, Opcode.PUSH_U32)
                    self.append_u32(bytecode, op.int_value)
                    self.append_opcode(bytecode, Opcode.CALL)
                elif op.type == OpType.RETURN:
                    self.append_opcode(bytecode, Opcode.RETURN)
                elif op.type == OpType.DROP:
                    self.append_opcode(bytecode, Opcode.DROP)
                elif op.type == OpType.DUPLICATE:
                    self.append_opcode(bytecode, Opcode.DUPLICATE)
                elif op.type == OpType.PUSH_LABEL:
                    self.append_opcode(bytecode, Opcode.PUSH_U32)
                    self.append_u32(bytecode, labels.get(op.str_value, 0))
                elif op.type == OpType.PUSH_INT:
                    self.append_opcode(bytecode, Opcode.PUSH_S32)
                    self.append_s32(bytecode, op.int_value)
                elif op.type == OpType.PUSH_CHR:
                    self.append_opcode(bytecode, Opcode.PUSH_U8)
                    self.append_u8(bytecode, ord(op.str_value) % 0xff)
                elif op.type == OpType.PUSH_STR:
                    self.append_opcode(bytecode, Opcode.PUSH_U32)
                    self.append_u32(
                            bytecode,
                            self.get_string_offset(op.str_value, strings)
                            + strings_pos)
                elif op.type == OpType.LOAD_LOCAL_OFFSET:
                    self.append_opcode(bytecode, Opcode.PUSH_U32)
                    self.append_u32(
                            bytecode, op.int_value + self.FRAME_HEADER_SIZE)
                    self.append_opcode(bytecode, Opcode.LOAD_LOCAL)
                elif op.type == OpType.STORE_LOCAL_OFFSET:
                    self.append_opcode(bytecode, Opcode.PUSH_U32)
                    self.append_u32(
                            bytecode, op.int_value + self.FRAME_HEADER_SIZE)
                    self.append_opcode(bytecode, Opcode.STORE_LOCAL)
                elif op.type == OpType.UNARY_DEREFERENCE:
                    self.append_opcode(bytecode, Opcode.UNARY_DEREFERENCE)
                elif op.type == OpType.UNARY_NEGATE:
                    self.append_opcode(bytecode, Opcode.UNARY_NEGATE)
                elif op.type == OpType.UNARY_NOT:
                    self.append_opcode(bytecode, Opcode.UNARY_NOT)
                elif op.type == OpType.BINARY_ADD:
                    self.append_opcode(bytecode, Opcode.BINARY_ADD)
                elif op.type == OpType.BINARY_SUBTRACT:
                    self.append_opcode(bytecode, Opcode.BINARY_SUBTRACT)
                elif op.type == OpType.BINARY_MULTIPLY:
                    self.append_opcode(bytecode, Opcode.BINARY_MULTIPLY)
                elif op.type == OpType.BINARY_DIVIDE:
                    self.append_opcode(bytecode, Opcode.BINARY_DIVIDE)
                elif op.type == OpType.BINARY_MODULO:
                    self.append_opcode(bytecode, Opcode.BINARY_MODULO)
                elif op.type == OpType.BINARY_EQUALS:
                    self.append_opcode(bytecode, Opcode.BINARY_EQUALS)
                elif op.type == OpType.BINARY_NOT_EQUALS:
                    self.append_opcode(bytecode, Opcode.BINARY_NOT_EQUALS)
                elif op.type == OpType.BINARY_GREATER:
                    self.append_opcode(bytecode, Opcode.BINARY_GREATER)
                elif op.type == OpType.BINARY_GREATER_EQUALS:
                    self.append_opcode(bytecode, Opcode.BINARY_GREATER_EQUALS)
                elif op.type == OpType.BINARY_LESS:
                    self.append_opcode(bytecode, Opcode.BINARY_LESS)
                elif op.type == OpType.BINARY_LESS_EQUALS:
                    self.append_opcode(bytecode, Opcode.BINARY_LESS_EQUALS)
                elif op.type == OpType.BINARY_AND:
                    self.append_opcode(bytecode, Opcode.BINARY_AND)
                elif op.type == OpType.BINARY_OR:
                    self.append_opcode(bytecode, Opcode.BINARY_OR)
                elif op.type == OpType.PUT_CHR:
                    self.append_opcode(bytecode, Opcode.PUT_CHR)
                else:
                    print(f"Unimplemented IR op type '{op}'!")
                    self.append_opcode(bytecode, Opcode.NO_OPERATION)
        
        for string in strings:
            for character in string:
                self.append_u8(bytecode, ord(character) % 0xff)
            
            self.append_u8(bytecode, 0x00)
        
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
