from enum import Enum, auto

class IROpType(Enum):
    """ The type of an IR operation. """
    
    HALT = auto()
    """ Pop and halt element. """
    
    NO_OPERATION = auto()
    """ Do nothing. """
    
    BRANCH_ALWAYS_LABEL = auto()
    """ Branch always with label. """
    
    CALL_ARGC = auto()
    """ Call with argument count. """
    
    RETURN = auto()
    """ Pop and return element. """
    
    PUSH_LABEL = auto()
    """ Push labeled address. """
    
    PUSH_INT = auto()
    """ Push integer value. """
    
    DISCARD = auto()
    """ Pop and discard element. """
    
    PRINT = auto()
    """ Pop and print element. """
