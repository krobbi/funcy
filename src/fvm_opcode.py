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
    PUSH_S32 = 0x0a
    DISCARD = 0x0b
    PRINT = 0x0c
