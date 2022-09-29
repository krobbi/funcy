from enum import Enum, auto

from ..parser.position import Span

class Node:
    """ A node of an abstract syntax tree. """
    
    span: Span
    """ The node's span. """
    
    def __init__(self) -> None:
        """ Initialize the node's span. """
        
        self.span = Span()


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


class AndExprNode(ExprNode):
    """ An and expression node of an abstract syntax tree. """
    
    lhs_expr: ExprNode
    """ The and expression's left hand side expression. """
    
    rhs_expr: ExprNode
    """ The and expression's right hand side expression. """
    
    def __init__(self, lhs_expr: ExprNode, rhs_expr: ExprNode) -> None:
        """ Initialize the and expression's expressions. """
        
        super().__init__()
        self.lhs_expr = lhs_expr
        self.rhs_expr = rhs_expr
    
    
    def __str__(self) -> str:
        """ Return the and expression's string. """
        
        return f"AndExpr @ ({self.span})"


class OrExprNode(ExprNode):
    """ An or expression node of an abstract syntax tree. """
    
    lhs_expr: ExprNode
    """ The or expression's left hand side expression. """
    
    rhs_expr: ExprNode
    """ The or expression's right hand side expression. """
    
    def __init__(self, lhs_expr: ExprNode, rhs_expr: ExprNode) -> None:
        """ Initialize the or expression's expressions. """
        
        super().__init__()
        self.lhs_expr = lhs_expr
        self.rhs_expr = rhs_expr
    
    
    def __str__(self) -> str:
        """ Return the and expression's string. """
        
        return f"OrExpr @ ({self.span})"


class AssignExprNode(ExprNode):
    """ An assign expression node of an abstract syntax tree. """
    
    lhs_expr: ExprNode
    """ The assign expression's left hand side expression. """
    
    rhs_expr: ExprNode
    """ The assign expression's right hand side expression. """
    
    def __init__(self, lhs_expr: ExprNode, rhs_expr: ExprNode) -> None:
        """ Initialize the assign expression's expressions. """
        
        super().__init__()
        self.lhs_expr = lhs_expr
        self.rhs_expr = rhs_expr
    
    
    def __str__(self) -> str:
        """ Return the assign expression's string. """
        
        return f"AssignExpr @ ({self.span})"


class UnOp(Enum):
    """ A unary operator. """
    
    AFFIRM = auto()
    """ `+x`. """
    
    NEGATE = auto()
    """ `-x`. """
    
    NOT = auto()
    """ `!x`. """


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


class BinOp(Enum):
    """ A binary operator. """
    
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
    """ `x == y`. """
    
    NOT_EQUALS = auto()
    """ `x != y`. """
    
    GREATER = auto()
    """ `x > y`. """
    
    GREATER_EQUALS = auto()
    """ `x >= y`. """
    
    LESS = auto()
    """ `x < y`. """
    
    LESS_EQUALS = auto()
    """ `x <= y`. """
    
    AND = auto()
    """ `x & y`. """
    
    OR = auto()
    """ `x | y`. """


class BinExprNode(ExprNode):
    """ A binary expression node of an abstract syntax tree. """
    
    lhs_expr: ExprNode
    """ The binary expression's left hand side expression. """
    
    op: BinOp
    """ The binary expression's operator. """
    
    rhs_expr: ExprNode
    """ The binary expression's right hand side expression. """
    
    def __init__(
            self, lhs_expr: ExprNode, op: BinOp, rhs_expr: ExprNode) -> None:
        """
        Initialize the binary expression's expressions and operator.
        """
        
        super().__init__()
        self.lhs_expr = lhs_expr
        self.op = op
        self.rhs_expr = rhs_expr
    
    
    def __str__(self) -> str:
        """ Return the binary expression's string. """
        
        return f"BinExpr: {self.op.name} @ ({self.span})"


class DeclNode(Node):
    """ A declaration node of an abstract syntax tree. """
    
    is_mutable: bool
    """ Whether the declaration is mutable. """
    
    name: str
    """ The declaration's name. """
    
    def __init__(self, is_mutable: bool, name: str) -> None:
        """ Initialize the declaration's mutability and name. """
        
        super().__init__()
        self.is_mutable = is_mutable
        self.name = name
    
    
    def __str__(self) -> str:
        result: str = "Decl: "
        
        if self.is_mutable:
            result += "Mutable"
        else:
            result += "Immutable"
        
        return f"{result} {self.name} @ ({self.span})"


class StmtNode(Node):
    """ A statement node of an abstract syntax tree. """


class FuncStmtNode(StmtNode):
    """ A function statement node of an abstract syntax tree. """
    
    name: IdentifierExprNode
    """ The function statement's name. """
    
    decls: list[DeclNode]
    """ The function statement's declarations. """
    
    stmt: StmtNode
    """ The function statement's statement. """
    
    def __init__(
            self, name: IdentifierExprNode, decls: list[DeclNode],
            stmt: StmtNode) -> None:
        """
        Initialize the function statement's name, declarations and
        statement.
        """
        
        super().__init__()
        self.name = name
        self.decls = decls
        self.stmt = stmt
    
    
    def __str__(self) -> str:
        """ Return the function statement's string. """
        
        return f"FuncStmt @ ({self.span})"


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


class IfStmtNode(StmtNode):
    """ An if statement node of an abstract syntax tree. """
    
    expr: ExprNode
    """ The if statement's expression. """
    
    stmt: StmtNode
    """ The if statement's statement. """
    
    def __init__(self, expr: ExprNode, stmt: StmtNode) -> None:
        """ Initialize the if statement's expression and statement. """
        
        super().__init__()
        self.expr = expr
        self.stmt = stmt
    
    
    def __str__(self) -> str:
        """ Return the if statement's string. """
        
        return f"IfStmt @ ({self.span})"


class IfElseStmtNode(StmtNode):
    """ An if else statement node of an abstract syntax tree. """
    
    expr: ExprNode
    """ The if else statement's expression. """
    
    then_stmt: StmtNode
    """ The if else statement's then statement. """
    
    else_stmt: StmtNode
    """ The if else statement's else statement. """
    
    def __init__(
            self, expr: ExprNode,
            then_stmt: StmtNode, else_stmt: StmtNode) -> None:
        """
        Initialize the if else statement's expression and statements.
        """
        
        super().__init__()
        self.expr = expr
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt
    
    
    def __str__(self) -> str:
        """ Return the if else statement's string. """
        
        return f"IfElseStmt @ ({self.span})"


class NopStmtNode(StmtNode):
    """ A no operation statement node of an abstract syntax tree. """
    
    def __str__(self) -> str:
        """ Return the no operation statement's string. """
        
        return f"NopStmt @ ({self.span})"


class LetStmtNode(StmtNode):
    """ A let statement node of an abstract syntax tree. """
    
    decl: DeclNode
    """ The let statement's declaration. """
    
    def __init__(self, decl: DeclNode) -> None:
        """ Initialize the let statement's declaration. """
        
        super().__init__()
        self.decl = decl
    
    
    def __str__(self) -> str:
        """ Return the let statement's string. """
        
        return f"LetStmt @ ({self.span})"


class LetExprStmtNode(StmtNode):
    """ A let expression statement node of an abstract syntax tree. """
    
    decl: DeclNode
    """ The let expression statement's declaration. """
    
    expr: ExprNode
    """ The let expression statement's expression. """
    
    def __init__(self, decl: DeclNode, expr: ExprNode) -> None:
        """
        Initialize the let expression statement's declaration and
        expression.
        """
        
        super().__init__()
        self.decl = decl
        self.expr = expr
    
    
    def __str__(self) -> str:
        """ Return the let expression statement's string. """
        
        return f"LetExprStmt @ ({self.span})"


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
