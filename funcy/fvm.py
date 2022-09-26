from enum import Enum

class Opcode(Enum):
    """ An FVM bytecode opcode. """
    
    HALT = 0x00
    NO_OPERATION = 0x01
    JUMP = 0x02
    JUMP_NOT_ZERO = 0x03
    JUMP_ZERO = 0x04
    CALL = 0x05
    RETURN = 0x06
    DROP = 0x07
    DUPLICATE = 0x08
    PUSH_U8 = 0x09
    PUSH_S8 = 0x0a
    PUSH_U16 = 0x0b
    PUSH_S16 = 0x0c
    PUSH_U32 = 0x0d
    PUSH_S32 = 0x0e
    LOAD_LOCAL = 0x0f
    STORE_LOCAL = 0x10
    UNARY_NEGATE = 0x11
    UNARY_NOT = 0x12
    BINARY_ADD = 0x13
    BINARY_SUBTRACT = 0x14
    BINARY_MULTIPLY = 0x15
    BINARY_DIVIDE = 0x16
    BINARY_MODULO = 0x17
    BINARY_EQUALS = 0x18
    BINARY_NOT_EQUALS = 0x19
    BINARY_GREATER = 0x1a
    BINARY_GREATER_EQUALS = 0x1b
    BINARY_LESS = 0x1c
    BINARY_LESS_EQUALS = 0x1d
    BINARY_AND = 0x1e
    BINARY_OR = 0x1f
    PRINT = 0x20


class FVM:
    """ The Funcy Virtual Machine """
    
    HEADER: bytes = bytes([0x83, 0x46, 0x56, 0x4d, 0x0d, 0x0a, 0x1a, 0x0a])
    """ An FVM bytecode file's header. """
    
    FORMAT_VERSION: int = 1
    """ The FVM's format version. """
    
    LEGAL_OPCODES: set[int] = set(opcode.value for opcode in Opcode)
    """ The FVM's legal opcodes. """
    
    ef: bool = False
    """ The FVM's execution flag. """
    
    ec: int = 0
    """ The FVM's exit code. """
    
    pm: bytes
    """ The FVM's program memory. """
    
    sm: list[int]
    """ The FVM's stack memory. """
    
    ip: int = 0
    """ The FVM's instruction pointer. """
    
    fp: int = 0
    """ The FVM's frame pointer. """
    
    def __init__(self) -> None:
        """ Initialize the FVM's memory. """
        
        self.pm = bytes([Opcode.PUSH_U8.value, 0x00, Opcode.HALT.value])
        self.sm = []
    
    
    def load(self, bytecode: bytes) -> bool:
        """ Load an FVM bytecode file's data. """
        
        if len(bytecode) < 16:
            return False
        elif bytecode[0:8] != self.HEADER:
            return False
        elif(
                int.from_bytes(bytecode[8:12], "little", signed=False)
                != self.FORMAT_VERSION):
            return False
        
        size: int = int.from_bytes(bytecode[12:16], "little", signed=False)
        
        if len(bytecode) < 16 + size:
            return False
        
        return self.load_flat(bytecode[16:16 + size])
    
    
    def load_flat(self, bytecode: bytes) -> bool:
        """ Load flat FVM bytecode. """
        
        if self.ef:
            return False
        
        self.pm = bytecode
        return True
    
    
    def begin(self) -> bool:
        """ Begin execution. """
        
        if self.ef:
            return False
        
        self.ip = 0
        self.sm = []
        self.fp = 0
        self.ec = 0
        self.ef = True
        return True
    
    
    def step(self) -> None:
        """ Step the FVM. """
        
        if not self.ef or not self.validate_fetch(1):
            return
        
        opcode_value: int = self.fetch_int(1, False)
        
        if not opcode_value in self.LEGAL_OPCODES:
            self.crash()
            return
        
        opcode: Opcode = Opcode(opcode_value)
        
        if opcode == Opcode.HALT and self.validate_pop(1):
            self.ec = self.sm.pop()
            self.ef = False
        elif opcode == Opcode.NO_OPERATION:
            pass
        elif opcode == Opcode.JUMP and self.validate_pop(1):
            self.ip = self.sm.pop()
        elif opcode == Opcode.JUMP_NOT_ZERO and self.validate_pop(2):
            jump_address: int = self.sm.pop()
            
            if self.sm.pop() != 0:
                self.ip = jump_address
        elif opcode == Opcode.JUMP_ZERO and self.validate_pop(2):
            jump_address: int = self.sm.pop()
            
            if self.sm.pop() == 0:
                self.ip = jump_address
        elif opcode == Opcode.CALL and self.validate_pop(2):
            param_count: int = self.sm.pop()
            call_address: int = self.sm.pop()
            
            if not self.validate_pop(param_count):
                return
            
            args: list[int] = []
            
            for i in range(param_count):
                args.insert(0, self.sm.pop())
            
            self.sm.append(self.fp)
            self.fp = len(self.sm) - 1
            self.sm.append(self.ip)
            self.ip = call_address
            self.sm.extend(args)
        elif opcode == Opcode.RETURN and self.validate_pop(1):
            old_fp: int = self.fp
            self.ip = self.sm[old_fp + 1]
            self.fp = self.sm[old_fp]
            return_value: int = self.sm.pop()
            self.sm = self.sm[0:old_fp]
            self.sm.append(return_value)
        elif opcode == Opcode.DROP and self.validate_pop(1):
            self.sm.pop()
        elif opcode == Opcode.DUPLICATE and self.validate_pop(1):
            self.sm.append(self.sm[-1])
        elif opcode == Opcode.PUSH_U8 and self.validate_fetch(1):
            self.sm.append(self.fetch_int(1, False))
        elif opcode == Opcode.PUSH_S8 and self.validate_fetch(1):
            self.sm.append(self.fetch_int(1, True))
        elif opcode == Opcode.PUSH_U16 and self.validate_fetch(2):
            self.sm.append(self.fetch_int(2, False))
        elif opcode == Opcode.PUSH_S16 and self.validate_fetch(2):
            self.sm.append(self.fetch_int(2, True))
        elif opcode == Opcode.PUSH_U32 and self.validate_fetch(4):
            self.sm.append(self.fetch_int(4, False))
        elif opcode == Opcode.PUSH_S32 and self.validate_fetch(4):
            self.sm.append(self.fetch_int(4, True))
        elif opcode == Opcode.LOAD_LOCAL and self.validate_pop(1):
            self.sm.append(self.sm[self.fp + self.sm.pop()])
        elif opcode == Opcode.STORE_LOCAL and self.validate_pop(2):
            store_offset: int = self.sm.pop()
            self.sm[self.fp + store_offset] = self.sm[-1]
        elif opcode == Opcode.UNARY_NEGATE and self.validate_pop(1):
            self.sm.append(-self.sm.pop())
        elif opcode == Opcode.UNARY_NOT and self.validate_pop(1):
            self.sm.append(int(self.sm.pop() == 0))
        elif opcode == Opcode.BINARY_ADD and self.validate_pop(2):
            y: int = self.sm.pop()
            x: int = self.sm.pop()
            self.sm.append(x + y)
        elif opcode == Opcode.BINARY_SUBTRACT and self.validate_pop(2):
            y: int = self.sm.pop()
            x: int = self.sm.pop()
            self.sm.append(x - y)
        elif opcode == Opcode.BINARY_MULTIPLY and self.validate_pop(2):
            y: int = self.sm.pop()
            x: int = self.sm.pop()
            self.sm.append(x * y)
        elif opcode == Opcode.BINARY_DIVIDE and self.validate_pop(2):
            y: int = self.sm.pop()
            
            if y == 0:
                self.crash()
                return
            
            x: int = self.sm.pop()
            self.sm.append(x // y)
        elif opcode == Opcode.BINARY_MODULO and self.validate_pop(2):
            y: int = self.sm.pop()
            
            if y == 0:
                self.crash()
                return
            
            x: int = self.sm.pop()
            self.sm.append(x % y)
        elif opcode == Opcode.BINARY_EQUALS and self.validate_pop(2):
            y: int = self.sm.pop()
            x: int = self.sm.pop()
            self.sm.append(int(x == y))
        elif opcode == Opcode.BINARY_NOT_EQUALS and self.validate_pop(2):
            y: int = self.sm.pop()
            x: int = self.sm.pop()
            self.sm.append(int(x != y))
        elif opcode == Opcode.BINARY_GREATER and self.validate_pop(2):
            y: int = self.sm.pop()
            x: int = self.sm.pop()
            self.sm.append(int(x > y))
        elif opcode == Opcode.BINARY_GREATER_EQUALS and self.validate_pop(2):
            y: int = self.sm.pop()
            x: int = self.sm.pop()
            self.sm.append(int(x >= y))
        elif opcode == Opcode.BINARY_LESS and self.validate_pop(2):
            y: int = self.sm.pop()
            x: int = self.sm.pop()
            self.sm.append(int(x < y))
        elif opcode == Opcode.BINARY_LESS_EQUALS and self.validate_pop(2):
            y: int = self.sm.pop()
            x: int = self.sm.pop()
            self.sm.append(int(x <= y))
        elif opcode == Opcode.BINARY_AND and self.validate_pop(2):
            y: int = self.sm.pop()
            x: int = self.sm.pop()
            self.sm.append(int(x != 0 and y != 0))
        elif opcode == Opcode.BINARY_OR and self.validate_pop(2):
            y: int = self.sm.pop()
            x: int = self.sm.pop()
            self.sm.append(int(x != 0 or y != 0))
        elif opcode == Opcode.PRINT and self.validate_pop(1):
            print(self.sm.pop())
        else:
            self.crash()
    
    
    def crash(self) -> None:
        """ Crash the FVM. """
        
        self.ec = 1
        self.ef = False
    
    
    def validate_fetch(self, amount: int) -> bool:
        """ Validate whether a fetch operation can be performed. """
        
        if self.ip < 0 or self.ip + amount > len(self.pm):
            self.crash()
            return False
        
        return True
    
    
    def validate_pop(self, amount: int) -> bool:
        """ Validate whether a pop operation can be performed. """
        
        if len(self.sm) < amount:
            self.crash()
            return False
        
        return True
    
    
    def fetch_int(self, size: int, is_signed: bool) -> int:
        """ Fetch an integer from program memory. """
        
        value: int = int.from_bytes(
                self.pm[self.ip:self.ip + size], "little", signed=is_signed)
        self.ip += size
        return value
