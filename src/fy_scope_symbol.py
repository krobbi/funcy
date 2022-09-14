from fy_scope_symbol_type import ScopeSymbolType

class ScopeSymbol:
    """ The usage of an identifier in a scope. """
    
    identifier: str
    """ The symbol's identifier. """
    
    type: ScopeSymbolType
    """ The symbol's type. """
    
    int_value: int = 0
    """ The symbol's integer value. """
    
    str_value: str = ""
    """ The symbol's string value. """
    
    def __init__(self, identifier: str, type: ScopeSymbolType) -> None:
        """ Initialize the symbol's identifier and type. """
        
        self.identifier = identifier
        self.type = type
