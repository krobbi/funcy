from fy_node import Node
from fy_node_stmt_compound import CompoundStmtNode

class FuncDeclNode(Node):
    """ A function declaration node of an abstract syntax tree. """
    
    name: str
    """ The function declaration's name. """
    
    params: list[str]
    """ The function declaration's parameter names. """
    
    stmt: CompoundStmtNode = CompoundStmtNode()
    """ The function declaration's body statement. """
    
    def __init__(self, name: str) -> None:
        """ Initialize the function declaration's name and parameter names. """
        
        super().__init__()
        self.name = name
        self.params = []
    
    
    def __repr__(self) -> str:
        """ Return the function declaration's string representation. """
        
        result: str = f"FuncDecl: {self.name}("
        
        for i, v in enumerate(self.params):
            result += v
            
            if i < len(self.params) - 1:
                result += ", "
        
        return result + ")"
    
    
    def get_children(self) -> list[CompoundStmtNode]:
        """ Get the function declaration's children as a list. """
        
        return [self.stmt]
