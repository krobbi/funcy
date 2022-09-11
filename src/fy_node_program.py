from fy_node import Node
from fy_node_decl_func import FuncDeclNode

class ProgramNode(Node):
    """ A program node of an abstract syntax tree. """
    
    func_decls: list[FuncDeclNode]
    """ The program's function declarations. """
    
    def __init__(self) -> None:
        """ Initialize the program's function declarations. """
        
        super().__init__()
        self.func_decls = []
    
    
    def __repr__(self) -> str:
        """ Return the program's string representation. """
        
        return "Program"
    
    
    def get_children(self) -> list[FuncDeclNode]:
        """ Get the program's children as a list. """
        
        return self.func_decls
