from enum import Enum, auto

from ..parser.position import Span

class Node:
    """ A node of an abstract syntax tree. """
    
    span: Span
    """ The node's span. """
    
    def __init__(self) -> None:
        """ Initialize the node's span. """
        
        self.span = Span()
    
    
    def __str__(self) -> str:
        """ Return the node's string. """
        
        result: str = self.__class__.__name__.removesuffix("Node")
        info: str = self.get_info()
        
        if info:
            result += f": {info}"
        
        return f"{result} @ ({self.span})"
    
    
    def get_info(self) -> str:
        """ Get information about the node. """
        
        return ""


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
    
    
    def get_info(self) -> str:
        """ Get information about the integer expression. """
        
        return str(self.value)


class ChrExprNode(ExprNode):
    """ A character expression node of an abstract syntax tree. """
    
    value: str
    """ The character expression's value. """
    
    def __init__(self, value: str) -> None:
        """ Initialize the character expression's value. """
        
        super().__init__()
        self.value = value
    
    
    def get_info(self) -> str:
        """ Get information about the character expression. """
        
        return self.value


class StrExprNode(ExprNode):
    """ A string expression node of an abstract syntax tree. """
    
    value: str
    """ The string expression's value. """
    
    def __init__(self, value: str) -> None:
        """ Initialize the string expression's value. """
        
        super().__init__()
        self.value = value
    
    
    def get_info(self) -> str:
        """ Get information about the string expression. """
        
        return self.value


class IdentifierExprNode(ExprNode):
    """ An identifier expression node of an abstract syntax tree. """
    
    name: str
    """ The identifier expression's name. """
    
    def __init__(self, name: str) -> None:
        """ Initialize the identifier expression's name. """
        
        super().__init__()
        self.name = name
    
    
    def get_info(self) -> str:
        """ Get information about the identifier expression. """
        
        return self.name


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


class AssignOp(Enum):
    """ An assignment operator. """
    
    SIMPLE = auto()
    """ `x = y`. """
    
    ADD = auto()
    """ `x += y`. """
    
    SUBTRACT = auto()
    """ `x -= y`. """
    
    MULTIPLY = auto()
    """ `x *= y`. """
    
    DIVIDE = auto()
    """ `x /= y`. """
    
    MODULO = auto()
    """ `x %= y`. """
    
    AND = auto()
    """ `x &= y`. """
    
    OR = auto()
    """ `x |= y`. """


class AssignExprNode(ExprNode):
    """ An assign expression node of an abstract syntax tree. """
    
    lhs_expr: ExprNode
    """ The assign expression's left hand side expression. """
    
    rhs_expr: ExprNode
    """ The assign expression's right hand side expression. """
    
    def __init__(
            self, lhs_expr: ExprNode, op: AssignOp,
            rhs_expr: ExprNode) -> None:
        """
        Initialize the assign expression's expressions and operator.
        """
        
        super().__init__()
        self.lhs_expr = lhs_expr
        self.op = op
        self.rhs_expr = rhs_expr
    
    
    def get_info(self) -> str:
        """ Get information about the assign expression. """
        
        return self.op.name


class UnOp(Enum):
    """ A unary operator. """
    
    DEREFERENCE = auto()
    """ `*x`. """
    
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
    
    
    def get_info(self) -> str:
        """ Get information about the unary expression. """
        
        return self.op.name


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
    
    
    def get_info(self) -> str:
        """ Get information about the binary expression. """
        
        return self.op.name


class IntrinsicExprNode(ExprNode):
    """ An intrinsic expression node of an abstract syntax tree. """
    
    name: IdentifierExprNode
    """ The intrinsic expression's name. """
    
    exprs: list[ExprNode]
    """ The intrinsic expression's expressions. """
    
    def __init__(self, name: IdentifierExprNode) -> None:
        """
        Initialize the intrinsic expression's name and expressions.
        """
        
        super().__init__()
        self.name = name
        self.exprs = []


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
    
    
    def get_info(self) -> str:
        """ Get information about the declaration. """
        
        result: str = "Mutable" if self.is_mutable else "Immutable"
        return f"{result} {self.name}"


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


class BlockStmtNode(StmtNode):
    """ A block statement node of an abstract syntax tree. """
    
    stmts: list[StmtNode]
    """ The block statement's statements. """
    
    def __init__(self) -> None:
        """ Initialize the block statement's statements. """
        
        super().__init__()
        self.stmts = []


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


class WhileStmtNode(StmtNode):
    """ A while statement node of an abstract syntax tree. """
    
    expr: ExprNode
    """ The while statement's expression. """
    
    stmt: StmtNode
    """ The while statement's statement. """
    
    def __init__(self, expr: ExprNode, stmt: StmtNode) -> None:
        """
        Initialize the while statement's expression and statement.
        """
        
        super().__init__()
        self.expr = expr
        self.stmt = stmt


class NopStmtNode(StmtNode):
    """ A no operation statement node of an abstract syntax tree. """


class LetStmtNode(StmtNode):
    """ A let statement node of an abstract syntax tree. """
    
    decl: DeclNode
    """ The let statement's declaration. """
    
    def __init__(self, decl: DeclNode) -> None:
        """ Initialize the let statement's declaration. """
        
        super().__init__()
        self.decl = decl


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


class ReturnStmtNode(StmtNode):
    """ A return statement node of an abstract syntax tree. """


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


class ScopedJumpStmt(StmtNode):
    """ A scoped jump statement node of an abstract syntax tree. """
    
    name: str
    """ The scoped jump statement's name. """
    
    def __init__(self, name: str) -> None:
        """ Initialize the scoped jump statement's name. """
        
        super().__init__()
        self.name = name
    
    
    def get_info(self) -> str:
        """ Get information about the scoped jump statement. """
        
        return self.name


class ExprStmtNode(StmtNode):
    """ An expression statement node of an abstract syntax tree. """
    
    expr: ExprNode
    """ The expression statement's expression. """
    
    def __init__(self, expr: ExprNode) -> None:
        """ Initialize the expression statement's expression. """
        
        super().__init__()
        self.expr = expr


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
