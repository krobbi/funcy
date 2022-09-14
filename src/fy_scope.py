from fy_scope_symbol import ScopeSymbol

class Scope:
    """ A level of scope definitions in a scope stack. """
    
    local_count: int
    """ The total number of local symbols available to the scope. """
    
    symbols: dict[str, ScopeSymbol]
    """ The scope's symbols. """
    
    def __init__(self, local_count: int) -> None:
        """ Initialize the scope's local symbol count and symbols. """
        
        self.local_count = local_count
        self.symbols = {}
