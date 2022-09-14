from fy_scope import Scope
from fy_scope_symbol import ScopeSymbol
from fy_scope_symbol_type import ScopeSymbolType

class ScopeStack:
    """ A stack of scopes. """
    
    scopes: list[Scope]
    """ The scope stack's scopes. """
    
    def __init__(self) -> None:
        """ Initialize the scope stack's scopes. """
        
        self.scopes = [Scope(0)]
    
    
    def __repr__(self) -> str:
        """ Return the scope stack's string representation. """
        
        return "ScopeStack"
    
    
    def get_symbol(self, identifier: str) -> ScopeSymbol:
        """ Get a symbol from the scope stack. """
        
        for i in range(len(self.scopes) - 1, -1, -1):
            scope: Scope = self.scopes[i]
            
            if identifier in scope.symbols:
                return scope.symbols[identifier]
        
        return ScopeSymbol(identifier, ScopeSymbolType.UNDEFINED)
    
    
    def has_symbol(self, identifier: str) -> bool:
        """ Return whether a symbol is defined in the current scope. """
        
        return identifier in self.scopes[-1].symbols
    
    
    def push_scope(self) -> None:
        """ Push a scope to the scope stack. """
        
        self.scopes.append(Scope(self.scopes[-1].local_count))
    
    
    def pop_scope(self) -> None:
        """ Pop a scope from the scope stack. """
        
        if len(self.scopes) > 1:
            self.scopes.pop()
        else:
            print("Codegen bug: Popped from an empty scope stack!")
    
    
    def undefine_locals(self) -> None:
        """ Undefine all local symbols from the current scope. """
        
        scope: Scope = self.scopes[-1]
        seen_identifiers: set[str] = set()
        scope.local_count = 0
        
        for identifier in set(key for key in scope.symbols):
            seen_identifiers.add(identifier)
            
            if scope.symbols[identifier].type == ScopeSymbolType.LOCAL:
                scope.symbols.pop(identifier)
                scope.symbols[identifier] = ScopeSymbol(identifier, ScopeSymbolType.UNDEFINED)
        
        for i in range(len(self.scopes) - 2, -1, -1):
            parent_scope: Scope = self.scopes[i]
            
            for identifier in parent_scope.symbols:
                if not identifier in seen_identifiers:
                    seen_identifiers.add(identifier)
                    
                    if parent_scope.symbols[identifier].type == ScopeSymbolType.LOCAL:
                        scope.symbols[identifier] = ScopeSymbol(
                                identifier, ScopeSymbolType.UNDEFINED)
    
    
    def define_label(self, identifier: str, label: str) -> None:
        """ Define a label symbol in the current scope. """
        
        if self.has_symbol(identifier):
            print(f"Codegen bug: Defined an already defined symbol '{identifier}'!")
        else:
            symbol: ScopeSymbol = ScopeSymbol(identifier, ScopeSymbolType.LABEL)
            symbol.str_value = label
            self.scopes[-1].symbols[identifier] = symbol
    
    
    def define_local(self, identifier: str) -> None:
        """ Define a local symbol in the current scope. """
        
        if self.has_symbol(identifier):
            print(f"Codegen bug: Defined an already defined symbol '{identifier}'!")
        else:
            scope: Scope = self.scopes[-1]
            symbol: ScopeSymbol = ScopeSymbol(identifier, ScopeSymbolType.LOCAL)
            symbol.int_value = scope.local_count
            scope.local_count += 1
            scope.symbols[identifier] = symbol
