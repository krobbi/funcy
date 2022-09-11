from fy_node_expr import ExprNode
from fy_node_stmt import StmtNode

class ExprStmtNode(StmtNode):
    """ An expression statement node of an abstract syntax tree. """
    
    expr: ExprNode
    """ The expression statement's expression. """
    
    def __init__(self, expr: ExprNode) -> None:
        """ Initialize the expression statement's expression. """
        
        super().__init__()
        self.expr = expr
    
    
    def __repr__(self) -> str:
        """ Return the expression statement's string representation. """
        
        return "ExprStmt"
    
    
    def get_children(self) -> list[ExprNode]:
        """ Get the expression statement's children as a list. """
        
        return [self.expr]
