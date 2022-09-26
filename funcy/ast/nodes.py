from enum import Enum, auto

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


class CallExprNode(ExprNode):
    """ A call expression node of an abstract syntax tree. """
    
    callee: ExprNode
    """ The call expression's callee expression. """
    
    params: list[ExprNode]
    """ The call expression's parameter expressions. """
    
    def __init__(self, callee: ExprNode) -> None:
        """ Initialize the call expression's expressions. """
        
        super().__init__()
        self.callee = callee
        self.params = []
    
    
    def __str__(self) -> str:
        """ Return the call expression's string. """
        
        return f"CallExpr @ ({self.span})"
    
    
    def get_children(self) -> list[ExprNode]:
        """ Get the call expression's children as a list. """
        
        result: list[ExprNode] = [self.callee]
        result.extend(self.params)
        return result


class UnOp(Enum):
    """ A unary operator. """
    
    NEGATE = auto()
    """ `-x`. """
    
    NOT = auto()
    """ `!x`. (Unimplemented.) """


class UnExprNode(ExprNode):
    """ A unary expression node of an abstract syntax tree. """
    
    expr: ExprNode
    """ The unary expression's expression. """
    
    op: UnOp
    """ The unary expression's operator. """
    
    def __init__(self, expr: ExprNode, op: UnOp) -> None:
        """
        Initialize the unary expression's expression and operator.
        """
        
        super().__init__()
        self.expr = expr
        self.op = op
    
    
    def __str__(self) -> str:
        """ Return the unary expression's string. """
        
        return f"UnExpr: {self.op.name} @ ({self.span})"
    
    
    def get_children(self) -> list[ExprNode]:
        """ Get the unary expression's children as a list. """
        
        return [self.expr]


class BinOp(Enum):
    """ A binary operator. """
    
    NONE = auto()
    """ Not a valid operator. Simplifies parsing. """
    
    ADD = auto()
    """ `x + y`. """
    
    SUBTRACT = auto()
    """ `x - y`. """
    
    MULTIPLY = auto()
    """ `x * y`. """
    
    DIVIDE = auto()
    """ `x / y`. """
    
    MODULO = auto()
    """ `x % y`. """
    
    EQUALS = auto()
    """ `x == y`. (Unimplemented.) """
    
    NOT_EQUALS = auto()
    """ `x != y`. (Unimplemented.) """
    
    GREATER = auto()
    """ `x > y`. (Unimplemented.) """
    
    GREATER_EQUALS = auto()
    """ `x >= y`. (Unimplemented.) """
    
    LESS = auto()
    """ `x < y`. (Unimplemented.) """
    
    LESS_EQUALS = auto()
    """ `x <= y`. (Unimplemented.) """
    
    AND = auto()
    """ `x (eager logical and) y`. (Unimplemented.) """
    
    OR = auto()
    """ `x (eager logical or) y`. (Unimplemented.) """


class BinExprNode(ExprNode):
    """ A binary expression node of an abstract syntax tree. """
    
    lhs: ExprNode
    """ The binary expression's left hand side expression. """
    
    op: BinOp
    """ The binary expression's operator. """
    
    rhs: ExprNode
    """ The binary expression's right hand side expression. """
    
    def __init__(self, lhs: ExprNode, op: BinOp, rhs: ExprNode) -> None:
        """
        Initialize the binary expression's expressions and operator.
        """
        
        super().__init__()
        self.lhs = lhs
        self.op = op
        self.rhs = rhs
    
    
    def __str__(self) -> str:
        """ Return the binary expression's string. """
        
        return f"BinExpr: {self.op.name} @ ({self.span})"
    
    
    def get_children(self) -> list[ExprNode]:
        """ Get the binary expression's children as a list. """
        
        return [self.lhs, self.rhs]


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


class ReturnStmtNode(StmtNode):
    """ A return statement node of an abstract syntax tree. """
    
    def __str__(self) -> str:
        """ Return the return statement's string. """
        
        return f"ReturnStmt @ ({self.span})"


class ReturnExprStmtNode(StmtNode):
    """
    A return expression statement node of an abstract syntax tree.
    """
    
    expr: ExprNode
    """ The return expression statement's expression. """
    
    def __init__(self, expr: ExprNode) -> None:
        """ Initialize the return expression statement's expression. """
        
        super().__init__()
        self.expr = expr
    
    
    def __str__(self) -> str:
        """ Return the return expression statement's string. """
        
        return f"ReturnExprStmt @ ({self.span})"
    
    
    def get_children(self) -> list[ExprNode]:
        """
        Get the return expression statement's children as a list.
        """
        
        return [self.expr]


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
    """
    A syntax error node. Error nodes should not be inserted into the
    abstract syntax tree, and are instead used to pass the results of
    parsing errors up the recursive descent parser until they can be
    logged and discarded.
    """
    
    message: str
    """ The syntax error's message. """
    
    def __init__(self, message: str) -> None:
        """ Initialize the syntax error's message. """
        
        super().__init__()
        self.message = message


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
