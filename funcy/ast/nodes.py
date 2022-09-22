from ..parser.position import Span

class Node:
    """ A node of an abstract syntax tree. """
    
    span: Span
    """ The node's span. """
    
    def __init__(self) -> None:
        """ Initialize the node's span. """
        
        self.span = Span()
    
    
    def get_children(self) -> list:
        """ Get the node's children as a list. """
        
        return []


class ExprNode(Node):
    """ An expression node of an abstract syntax tree. """


class IntExprNode(ExprNode):
    """ An integer expression node of an abstract syntax tree. """
    
    value: int
    """ The integer expression's value. """
    
    def __init__(self, value: int) -> None:
        """ Initialize the integer expression's value. """
        
        super().__init__()
        self.value = value
    
    
    def __str__(self) -> str:
        """ Return the integer expression's string. """
        
        return f"IntExpr: {self.value} @ ({self.span})"


class IdentifierExprNode(ExprNode):
    """ An identifier expression node of an abstract syntax tree. """
    
    name: str
    """ The identifier expression's name. """
    
    def __init__(self, name: str) -> None:
        """ Initialize the identifier expression's name. """
        
        super().__init__()
        self.name = name
    
    
    def __str__(self) -> str:
        """ Return the identifier expression's string. """
        
        return f"IdentifierExpr: {self.name} @ ({self.span})"


class StmtNode(Node):
    """ A statement node of an abstract syntax tree. """


class FuncStmtNode(StmtNode):
    """ A function statement node of an abstract syntax tree. """
    
    name: IdentifierExprNode
    """ The function statement's name. """
    
    params: list[IdentifierExprNode]
    """ The function statement's parameters. """
    
    stmt: StmtNode
    """ The function statement's statement. """
    
    def __init__(
            self, name: IdentifierExprNode, params: list[IdentifierExprNode],
            stmt: StmtNode) -> None:
        """
        Initialize the function statement's name, parameters and
        statement.
        """
        
        super().__init__()
        self.name = name
        self.params = params
        self.stmt = stmt
    
    
    def __str__(self) -> str:
        """ Return the function statement's string. """
        
        return f"FuncStmt @ ({self.span})"
    
    
    def get_children(self) -> list[Node]:
        """ Get the function statement's children as a list. """
        
        result: list[Node] = [self.name]
        result.extend(self.params)
        result.append(self.stmt)
        return result


class BlockStmtNode(StmtNode):
    """ A block statement node of an abstract syntax tree. """
    
    stmts: list[StmtNode]
    """ The block statement's statements. """
    
    def __init__(self) -> None:
        """ Initialize the block statement's statements. """
        
        super().__init__()
        self.stmts = []
    
    
    def __str__(self) -> str:
        """ Return the block statement's string. """
        
        return f"BlockStmt @ ({self.span})"
    
    
    def get_children(self) -> list[StmtNode]:
        """ Get the block statement's children as a list. """
        
        return self.stmts


class NopStmtNode(StmtNode):
    """ A no operation statement node of an abstract syntax tree. """
    
    def __str__(self) -> str:
        """ Return the no operation statement's string. """
        
        return f"NopStmt @ ({self.span})"


class PrintStmtNode(StmtNode):
    """ A print statement node of an abstract syntax tree. """
    
    expr: ExprNode
    """ The print statement's expression. """
    
    def __init__(self, expr: ExprNode) -> None:
        """ Initialize the print statement's expression. """
        
        super().__init__()
        self.expr = expr
    
    
    def __str__(self) -> str:
        """ Return the print statement's string. """
        
        return f"PrintStmt @ ({self.span})"
    
    
    def get_children(self) -> list[ExprNode]:
        """ Return the print statement's children as a list. """
        
        return [self.expr]


class ExprStmtNode(StmtNode):
    """ An expression statement node of an abstract syntax tree. """
    
    expr: ExprNode
    """ The expression statement's expression. """
    
    def __init__(self, expr: ExprNode) -> None:
        """ Initialize the expression statement's expression. """
        
        super().__init__()
        self.expr = expr
    
    
    def __str__(self) -> str:
        """ Return the expression statement's string. """
        
        return f"ExprStmt @ ({self.span})"
    
    
    def get_children(self) -> list[ExprNode]:
        """ Get the expression statement's children as a list. """
        
        return [self.expr]


class ErrorNode(Node):
    """ A syntax error node of an abstract syntax tree. """
    
    message: str
    """ The syntax error's message. """
    
    def __init__(self, message: str) -> None:
        """ Initialize the syntax error's message. """
        
        super().__init__()
        self.message = message
    
    
    def __str__(self) -> str:
        """ Return the syntax error's string. """
        
        return f"Error: {self.message} @ ({self.span})"


class RootNode(Node):
    """ A root node of an abstract syntax tree. """
    
    stmts: list[FuncStmtNode]
    """ The root's statements. """
    
    def __init__(self) -> None:
        """ Initialize the root's statements. """
        
        super().__init__()
        self.stmts = []
    
    
    def __str__(self) -> str:
        """ Return the root's string. """
        
        return f"Root @ ({self.span})"
    
    
    def get_children(self) -> list[FuncStmtNode]:
        """ Get the root's children as a list. """
        
        return self.stmts
