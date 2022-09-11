from fy_node_expr import ExprNode
from fy_node_stmt_expr import ExprStmtNode

class PrintExprStmtNode(ExprStmtNode):
    """ A print expression statement node of an abstract syntax tree. """
    
    def __init__(self, expr: ExprNode) -> None:
        """ Initialize the print expression statement's expression. """
        
        super().__init__(expr)
    
    
    def __repr__(self) -> str:
        """ Return the print expression statement's string representation. """
        
        return "PrintExprStmt"
