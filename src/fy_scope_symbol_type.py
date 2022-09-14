from enum import Enum, auto

class ScopeSymbolType(Enum):
    """ The type of a symbol. """
    
    UNDEFINED = auto()
    """ Undeclared or unavailable identifier. """
    
    LABEL = auto()
    """ Labeled address. """
    
    LOCAL = auto()
    """ Local variable or function parameter. """
