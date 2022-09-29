from enum import Enum, auto

from ..io.log import Log

class SymbolAccess(Enum):
    """ How a symbol is accessed. """
    
    UNDEFINED = auto()
    """ Undeclared or unavailable name. """
    
    FUNC = auto()
    """ Labeled function address with parameter count. """
    
    LOCAL = auto()
    """ Immutable local variable or function parameter. """
    
    LOCAL_MUT = auto()
    """ Mutable local variable or function parameter. """


class Symbol:
    """ The usage of a name in a scope. """
    
    name: str
    """ The symbol's name. """
    
    access: SymbolAccess
    """ The symbol's access. """
    
    int_value: int = 0
    """ The symbol's integer value. """
    
    str_value: str = ""
    """ The symbol's string value. """
    
    def __init__(self, name: str, access: SymbolAccess) -> None:
        """ Initialize the symbol's name and access. """
        
        self.name = name
        self.access = access


class Scope:
    """ A level of symbol definitions in a scope stack. """
    
    local_count: int
    """ The total number of local symbols available to the scope. """
    
    scope_local_count: int = 0
    """ The number of locals pushed at this level of the scope. """
    
    symbols: dict[str, Symbol]
    """ The scope's symbols. """
    
    def __init__(self, local_count: int) -> None:
        """ Initialize the scope's local symbol count and symbols. """
        
        self.local_count = local_count
        self.symbols = {}


class ScopeStack:
    """ A stack of scopes. """
    
    log: Log
    """ The scope stack's log. """
    
    scopes: list[Scope]
    """ The scope stack's scopes. """
    
    def __init__(self, log: Log) -> None:
        """ Initialize the scope stack's log and scopes. """
        
        self.log = log
        self.clear()
    
    
    def get(self, name: str) -> Symbol:
        """ Get a symbol from its name. """
        
        for i in range(len(self.scopes) - 1, -1, -1):
            scope: Scope = self.scopes[i]
            
            if name in scope.symbols:
                return scope.symbols[name]
        
        return Symbol(name, SymbolAccess.UNDEFINED)
    
    
    def get_scope_local_count(self) -> int:
        """ Get the number of locals pushed at the current scope. """
        
        return self.scopes[-1].scope_local_count
    
    
    def has(self, name: str) -> bool:
        """ Return whether a symbol is defined in the current scope. """
        
        return name in self.scopes[-1].symbols
    
    
    def clear(self) -> None:
        """ Clear the scope stack. """
        
        self.scopes = [Scope(0)]
    
    
    def push(self) -> None:
        """ Push a new scope to the top of the scope stack. """
        
        self.scopes.append(Scope(self.scopes[-1].local_count))
    
    
    def pop(self) -> None:
        """ Pop the top scope from the scope stack. """
        
        if len(self.scopes) <= 1:
            self.log.log("Bug: Popped an empty scope stack!")
            return
        
        self.scopes.pop()
    
    
    def undefine_locals(self) -> None:
        """ Undefine all locals in the current scope. """
        
        scope: Scope = self.scopes[-1]
        seen_names: set[str] = set()
        
        for name in set(key for key in scope.symbols):
            seen_names.add(name)
            
            if scope.symbols[name].access == SymbolAccess.LOCAL:
                scope.symbols.pop(name)
                scope.symbols[name] = Symbol(name, SymbolAccess.UNDEFINED)
        
        for i in range(len(self.scopes) - 2, -1, -1):
            parent: Scope = self.scopes[i]
            
            for name in parent.symbols:
                if name in seen_names:
                    continue
                
                seen_names.add(name)
                
                if parent.symbols[name].access == SymbolAccess.LOCAL:
                    scope.symbols[name] = Symbol(name, SymbolAccess.UNDEFINED)
        
        scope.local_count = 0
    
    
    def define_func(self, name: str, label: str, param_count: int) -> None:
        """ Define a function in the current scope. """
        
        if self.has(name):
            self.log.log(f"Bug: Function name '{name}' is already defined!")
            return
        
        symbol: Symbol = Symbol(name, SymbolAccess.FUNC)
        symbol.str_value = label
        symbol.int_value = param_count
        self.scopes[-1].symbols[name] = symbol
    
    
    def define_local(self, name: str) -> None:
        """ Define an immutable local in the current scope. """
        
        if self.has(name):
            self.log.log(
                    f"Bug: Local immutable name '{name}' is already defined!")
            return
        
        scope: Scope = self.scopes[-1]
        symbol: Symbol = Symbol(name, SymbolAccess.LOCAL)
        symbol.int_value = scope.local_count
        scope.local_count += 1
        scope.scope_local_count += 1
        scope.symbols[name] = symbol
    
    
    def define_local_mut(self, name: str) -> None:
        """ Define a mutable local in the current scope. """
        
        if self.has(name):
            self.log.log(
                    f"Bug: Local mutable name '{name}' is already defined!")
            return
        
        scope: Scope = self.scopes[-1]
        symbol: Symbol = Symbol(name, SymbolAccess.LOCAL_MUT)
        symbol.int_value = scope.local_count
        scope.local_count += 1
        scope.scope_local_count += 1
        scope.symbols[name] = symbol
