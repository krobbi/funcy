from enum import Enum

class Opcode(Enum):
    """ An FVM bytecode opcode. """
    
    HALT = 0x00
    NO_OPERATION = 0x01
    BRANCH_ALWAYS = 0x02
    CALL = 0x03
    RETURN = 0x04
    PUSH_U8 = 0x05
    PUSH_S8 = 0x06
    PUSH_U16 = 0x07
    PUSH_S16 = 0x08
    PUSH_U32 = 0x09
    PUSH_S32 = 0xa0
    DISCARD = 0x0b
    PRINT = 0x0c


class FVM:
    """ The Funcy Virtual Machine """
    
    HEADER: bytes = bytes([0x83, 0x46, 0x56, 0x4d, 0x0d, 0x0a, 0x1a, 0x0a])
    """ An FVM bytecode file's header. """
    
    FORMAT_VERSION: int = 0
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
        elif opcode == Opcode.BRANCH_ALWAYS and self.validate_pop(1):
            self.ip = self.sm.pop()
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
        elif opcode == Opcode.DISCARD and self.validate_pop(1):
            self.sm.pop()
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
