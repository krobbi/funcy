from fy_node_expr import ExprNode

class IntExprNode(ExprNode):
    """ An integer expression node of an abstract syntax tree. """
    
    value: int
    """ The integer expression's value. """
    
    def __init__(self, value: int) -> None:
        """ Initialize the integer expression's value. """
        
        super().__init__()
        self.value = value
    
    
    def __repr__(self) -> str:
        """ Return the integer expression's string representation. """
        
        return f"IntExpr: {self.value}"
