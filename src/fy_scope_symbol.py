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
    
    
    def __repr__(self) -> str:
        """ Return the symbol's string representation. """
        
        if self.type == ScopeSymbolType.LABEL:
            return f"ScopeSymbol({self.identifier}): {self.type.name}({self.str_value})"
        elif self.type == ScopeSymbolType.LOCAL:
            return f"ScopeSymbol({self.identifier}): {self.type.name}({self.int_value})"
        else:
            return f"ScopeSymbol({self.identifier}): {self.type.name}"
