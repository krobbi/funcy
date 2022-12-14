from collections.abc import Callable

from ..ast.nodes import *
from ..io.log import Log
from .lexer import Lexer
from .position import Position, Span
from .std import FUNCY_STANDARD_LIBRARY
from .token import Token, TokenType

class Parser:
    """ Parses an abstract syntax tree from source code. """
    
    is_parsing_std: bool = False
    """ Whether the parser is parsing the standard library. """
    
    log: Log
    """ The parser's log. """
    
    lexer: Lexer
    """ The parser's lexer. """
    
    next: Token
    """ The next token to accept. """
    
    current: Token
    """ The currently accepted token. """
    
    span_stack: list[Span]
    """ A stack of node start position spans. """
    
    def __init__(self, log: Log) -> None:
        """
        Initialize the parser's log, lexer, tokens and span stack.
        """
        
        self.log = log
        self.lexer = Lexer()
        self.next = Token(TokenType.EOF, Span())
        self.current = Token(TokenType.EOF, Span())
        self.span_stack = []
    
    
    def parse(self, source: str) -> RootNode:
        """ Parse an abstract syntax tree from source code. """
        
        root: RootNode = RootNode()
        root.modules.append(self.parse_module("std", FUNCY_STANDARD_LIBRARY))
        root.modules.append(self.parse_module("main", source))
        return root
    
    
    def parse_module(self, name: str, source: str) -> ModuleNode:
        """ Parse a module from a name and source code. """
        
        self.is_parsing_std = name == "std"
        self.lexer.begin(source)
        self.next = Token(TokenType.EOF, Span())
        self.advance()
        self.span_stack = []
        self.begin()
        module: ModuleNode = ModuleNode()
        
        while self.next.type != TokenType.EOF:
            if self.next.type == TokenType.KEYWORD_INCLUDE:
                if module.stmts:
                    self.log_error(
                            "Cannot use 'include' "
                            "after the first function of a module!", self.next)
                
                incl: Node = self.parse_incl()
                
                if isinstance(incl, InclNode):
                    module.incls.append(incl)
                else:
                    self.log_error(incl)
                
                continue
            
            stmt: Node = self.parse_stmt_func()
            
            if not isinstance(stmt, FuncStmtNode):
                if self.is_parsing_std:
                    self.log_error(
                            f"Bug: Bug in standard library at '{stmt}'!", stmt)
                
                self.log_error(stmt)
                continue
            
            module.stmts.append(stmt)
        
        return self.end(module)
    
    
    def parse_incl(self):
        """ Parse an inclusion. """
        
        self.begin()
        
        if not self.accept(TokenType.KEYWORD_INCLUDE):
            node: ErrorNode = ErrorNode("Expected 'include'!")
            node.span.replicate(self.next.span)
            return self.abort(node)
        
        if not self.accept(TokenType.LITERAL_STR):
            node: ErrorNode = ErrorNode(
                    "Expected a string literal for an inclusion!")
            node.span.replicate(self.next.span)
            return self.abort(node)
        
        node: InclNode = InclNode(self.current.str_value)
        
        if not self.accept(TokenType.SEMICOLON):
            self.log_error(
                    "Missing closing ';' in inclusion!", self.current.span.end)
        
        return self.end(node)
    
    
    def log_error(
            self, error: str | Token | Node,
            span: Position | Span | Token | Node = None) -> None:
        """ Log an error object. """
        
        if isinstance(span, Position):
            new_span: Span = Span()
            new_span.end.replicate(span)
            new_span.start.replicate(span)
            span = new_span
        elif isinstance(span, Span):
            span = span.copy()
        elif isinstance(span, Token):
            span = span.span.copy()
        elif isinstance(span, Node):
            span = span.span.copy()
        elif not span is None:
            self.log.log(f"Bug: Logged an error with a non-span '{span}'!")
            span = None
        
        if isinstance(error, str):
            self.log.log(error, span)
        elif isinstance(error, Token):
            if span is None:
                span = error.span.copy()
            
            if error.type == TokenType.ERROR:
                self.log.log(error.str_value, span)
            else:
                self.log.log(f"Bug: Logged a non-error token '{error}'!", span)
        elif isinstance(error, Node):
            if span is None:
                span = error.span.copy()
            
            if isinstance(error, ErrorNode):
                self.log.log(error.message, span)
            else:
                self.log.log(f"Bug: Logged a non-error node '{error}'!", span)
        else:
            self.log.log(f"Bug: Logged a non-error object '{error}'!", span)
    
    
    def begin(self) -> None:
        """ Begin a node's position at the next token. """
        
        self.span_stack.append(self.next.span.copy())
    
    
    def apply(self, node: Node) -> None:
        """ Apply a node's position without popping the span stack. """
        
        node.span.replicate(self.span_stack[-1])
        node.span.include(self.current.span)
    
    
    def end(self, node: Node) -> Node:
        """ End a node's position at the current token. """
        
        self.apply(node)
        self.span_stack.pop()
        return node
    
    
    def abort(self, node: Node) -> Node:
        """ Abort the position in the span stack. """
        
        self.span_stack.pop()
        return node
    
    
    def advance(self) -> None:
        """ Advance to the next token. """
        
        self.current = self.next
        self.next = self.lexer.get_token()
        
        while self.next.type == TokenType.ERROR:
            self.log_error(self.next)
            self.next = self.lexer.get_token()
    
    
    def accept(self, type: TokenType) -> bool:
        """ Accept the next token from its type. """
        
        if self.next.type != type:
            return False
        
        self.advance()
        return True
    
    
    def parse_stmt(self) -> Node:
        """ Parse a statement. """
        
        self.begin()
        
        if self.next.type == TokenType.KEYWORD_FUNC:
            return self.end(self.parse_stmt_func())
        elif self.next.type == TokenType.BRACE_OPEN:
            return self.end(self.parse_stmt_block())
        elif self.accept(TokenType.KEYWORD_IF):
            expr: Node = self.parse_expr_paren()
            stmt: Node = self.parse_stmt()
            
            if not isinstance(expr, ExprNode):
                return self.abort(expr)
            
            if not isinstance(stmt, StmtNode):
                return self.abort(stmt)
            
            if not self.accept(TokenType.KEYWORD_ELSE):
                return self.end(IfStmtNode(expr, stmt))
            
            else_stmt: Node = self.parse_stmt()
            
            if not isinstance(else_stmt, StmtNode):
                return self.abort(else_stmt)
            
            return self.end(IfElseStmtNode(expr, stmt, else_stmt))
        elif self.accept(TokenType.KEYWORD_WHILE):
            expr: Node = self.parse_expr_paren()
            stmt: Node = self.parse_stmt()
            
            if not isinstance(expr, ExprNode):
                return self.abort(expr)
            
            if not isinstance(stmt, StmtNode):
                return self.abort(stmt)
            
            return self.end(WhileStmtNode(expr, stmt))
        elif self.accept(TokenType.SEMICOLON):
            return self.end(NopStmtNode())
        elif self.accept(TokenType.KEYWORD_LET):
            decl: DeclNode = self.parse_decl()
            
            if not isinstance(decl, DeclNode):
                return self.abort(decl)
            
            if self.accept(TokenType.SEMICOLON):
                return self.end(LetStmtNode(decl))
            
            if not self.accept(TokenType.EQUALS):
                self.log_error(
                        "Missing ';' or '=' in let statement!",
                        self.current.span.end)
            
            expr: Node = self.parse_expr()
            has_semicolon: bool = self.accept(TokenType.SEMICOLON)
            
            if not isinstance(expr, ExprNode):
                self.log_error(expr)
                return self.end(LetStmtNode(decl))
            
            if not has_semicolon:
                self.log_error(
                        "Missing closing ';' in let statement!",
                        self.current.span.end)
            
            return self.end(LetExprStmtNode(decl, expr))
        elif self.accept(TokenType.KEYWORD_RETURN):
            if self.accept(TokenType.SEMICOLON):
                return self.end(ReturnStmtNode())
            
            expr: Node = self.parse_expr()
            has_semicolon: bool = self.accept(TokenType.SEMICOLON)
            
            if not isinstance(expr, ExprNode):
                self.log_error(expr)
                return self.end(ReturnStmtNode())
            
            if not has_semicolon:
                self.log_error(
                        "Missing closing ';' in return statement!",
                        self.current.span.end)
            
            return self.end(ReturnExprStmtNode(expr))
        elif self.accept(TokenType.KEYWORD_BREAK):
            if not self.accept(TokenType.SEMICOLON):
                self.log_error(
                        "Missing closing ';' in break statement!",
                        self.current.span.end)
            
            return self.end(ScopedJumpStmt("break"))
        elif self.accept(TokenType.KEYWORD_CONTINUE):
            if not self.accept(TokenType.SEMICOLON):
                self.log_error(
                        "Missing closing ';' in continue statement!",
                        self.current.span.end)
            
            return self.end(ScopedJumpStmt("continue"))
        
        expr: Node = self.parse_expr(True)
        has_semicolon: bool = self.accept(TokenType.SEMICOLON)
        
        if not isinstance(expr, ExprNode):
            return self.end(expr)
        
        if not has_semicolon:
            self.log_error(
                    "Missing closing ';' in expression statement!",
                    self.current.span.end)
        
        return self.end(ExprStmtNode(expr))
    
    
    def parse_stmt_func(self) -> Node:
        """ Parse a function statement. """
        
        self.begin()
        has_advanced: bool = self.accept(TokenType.KEYWORD_FUNC)
        
        if not has_advanced:
            self.log_error(
                    "Missing 'func' in function statement!",
                    self.next.span.start)
        
        if self.accept(TokenType.KEYWORD_MUT):
            self.log_error("Function names cannot be mutable!", self.current)
            has_advanced = True
        
        if not self.accept(TokenType.IDENTIFIER):
            node: ErrorNode = ErrorNode(
                    "Expected an identifier for a function name!")
            node.span.replicate(self.next.span)
            
            if not has_advanced:
                self.advance()
            
            return self.abort(node)
        
        name: IdentifierExprNode = IdentifierExprNode(self.current.str_value)
        name.span.replicate(self.current.span)
        decls: list[DeclNode] = []
        
        if not self.accept(TokenType.PARENTHESIS_OPEN):
            self.log_error(
                    f"Missing opening '(' in {name.name}'s parameter list!",
                    self.current.span.end)
        
        if self.next.type != TokenType.PARENTHESIS_CLOSE:
            decl: Node = self.parse_decl()
            
            if isinstance(decl, DeclNode):
                decls.append(decl)
            else:
                self.log_error(decl)
            
            while self.accept(TokenType.COMMA):
                decl = self.parse_decl()
                
                if isinstance(decl, DeclNode):
                    decls.append(decl)
                else:
                    self.log_error(decl)
        
        if not self.accept(TokenType.PARENTHESIS_CLOSE):
            self.log_error(
                    f"Missing closing ')' in {name.name}'s parameter list!",
                    self.current.span.end)
        
        if self.next.type != TokenType.BRACE_OPEN:
            stmt: Node = self.parse_stmt()
            
            if not isinstance(stmt, StmtNode):
                return self.abort(stmt)
            
            self.log_error(
                    f"Expected a block statement for {name.name}'s body!",
                    stmt)
            return self.end(FuncStmtNode(name, decls, stmt))
        
        stmt: Node = self.parse_stmt_block()
        
        if not isinstance(stmt, StmtNode):
            return self.abort(stmt)
        
        return self.end(FuncStmtNode(name, decls, stmt))
    
    
    def parse_stmt_block(self) -> Node:
        """ Parse a block statement. """
        
        self.begin()
        
        if not self.accept(TokenType.BRACE_OPEN):
            self.log_error(
                    "Missing opening '{' in block statement!",
                    self.current.span.end)
        
        open_span: Span = self.current.span
        block_stmt: BlockStmtNode = BlockStmtNode()
        
        while not self.accept(TokenType.BRACE_CLOSE):
            if self.next.type == TokenType.EOF:
                self.log_error(
                        "Missing closing '}' in block statement!", open_span)
                break
            
            stmt: Node = self.parse_stmt()
            
            if not isinstance(stmt, StmtNode):
                self.log_error(stmt)
                continue
            
            block_stmt.stmts.append(stmt)
        
        return self.end(block_stmt)
    
    
    def parse_decl(self) -> Node:
        """ Parse a declaraion. """
        
        is_mutable: bool = self.accept(TokenType.KEYWORD_MUT)
        
        self.begin()
        
        if not self.accept(TokenType.IDENTIFIER):
            node: ErrorNode = ErrorNode(
                    "Expected an identifier for a declaration!")
            node.span.replicate(self.next.span)
            return self.abort(node)
        
        return self.end(DeclNode(is_mutable, self.current.str_value))
    
    
    def parse_expr_paren(self) -> Node:
        """ Parse a parenthetical expression. """
        
        self.begin()
        
        if not self.accept(TokenType.PARENTHESIS_OPEN):
            self.log_error(
                    "Missing opening '(' in parenthetical expression!",
                    self.current.span.end)
        
        if self.accept(TokenType.PARENTHESIS_CLOSE):
            return self.end(ErrorNode(
                    "Missing expression in parenthetical expression!"))
        
        expr: Node = self.parse_expr()
        
        if not self.accept(TokenType.PARENTHESIS_CLOSE):
            self.log_error(
                    "Missing closing ')' in parenthetical expression!",
                    self.current.span.end)
        
        return self.abort(expr) # Exclude parentheses from span.
    
    
    def parse_expr(self, is_stmt: bool = False) -> Node:
        """ Parse an expression. """
        
        return self.parse_expr_assignment(is_stmt)
    
    
    def parse_expr_bin(
            self, is_stmt: bool, child_parser: Callable[[bool], Node],
            ops: dict[TokenType, BinOp]) -> Node:
        """ Parse a generic binary expression. """
        
        self.begin()
        expr: Node = child_parser(is_stmt)
        
        if not isinstance(expr, ExprNode):
            return self.abort(expr)
        
        while self.next.type in ops:
            self.advance()
            op: BinOp = ops[self.current.type]
            rhs_expr: Node = child_parser(False)
            
            if not isinstance(rhs_expr, ExprNode):
                return self.abort(rhs_expr)
            
            expr = BinExprNode(expr, op, rhs_expr)
            self.apply(expr)
        
        return self.abort(expr)
    
    
    def parse_expr_assignment(self, is_stmt: bool = False) -> Node:
        """ Parse an assignment expression. """
        
        self.begin()
        expr: Node = self.parse_expr_logical_or(is_stmt)
        
        if not isinstance(expr, ExprNode):
            return self.abort(expr)
        
        OPS: dict[TokenType, AssignOp] = {
            TokenType.PERCENT_EQUALS: AssignOp.MODULO,
            TokenType.AMPERSAND_EQUALS: AssignOp.AND,
            TokenType.STAR_EQUALS: AssignOp.MULTIPLY,
            TokenType.PLUS_EQUALS: AssignOp.ADD,
            TokenType.MINUS_EQUALS: AssignOp.SUBTRACT,
            TokenType.SLASH_EQUALS: AssignOp.DIVIDE,
            TokenType.EQUALS: AssignOp.SIMPLE,
            TokenType.PIPE_EQUALS: AssignOp.OR,
        }
        
        if self.next.type in OPS:
            self.advance()
            op: AssignOp = OPS[self.current.type]
            rhs_expr: Node = self.parse_expr_assignment()
            
            if not isinstance(rhs_expr, ExprNode):
                return self.abort(rhs_expr)
            
            expr = AssignExprNode(expr, op, rhs_expr)
            self.apply(expr)
        
        return self.abort(expr)
    
    
    def parse_expr_logical_or(self, is_stmt: bool = False) -> Node:
        """ Parse a logical or expression. """
        
        self.begin()
        expr: Node = self.parse_expr_logical_and(is_stmt)
        
        if not isinstance(expr, ExprNode):
            return self.abort(expr)
        
        while self.accept(TokenType.PIPE_PIPE):
            rhs_expr: Node = self.parse_expr_logical_and()
            
            if not isinstance(rhs_expr, ExprNode):
                return self.abort(rhs_expr)
            
            expr = OrExprNode(expr, rhs_expr)
            self.apply(expr)
        
        return self.abort(expr)
    
    
    def parse_expr_logical_and(self, is_stmt: bool = False) -> Node:
        """ Parse a logical and expression. """
        
        self.begin()
        expr: Node = self.parse_expr_eager_or(is_stmt)
        
        if not isinstance(expr, ExprNode):
            return self.abort(expr)
        
        while self.accept(TokenType.AMPERSAND_AMPERSAND):
            rhs_expr: Node = self.parse_expr_eager_or()
            
            if not isinstance(rhs_expr, ExprNode):
                return self.abort(rhs_expr)
            
            expr = AndExprNode(expr, rhs_expr)
            self.apply(expr)
        
        return self.abort(expr)
    
    
    def parse_expr_eager_or(self, is_stmt: bool = False) -> Node:
        """ Parse an eager or expression. """
        
        return self.parse_expr_bin(is_stmt, self.parse_expr_eager_and, {
            TokenType.PIPE: BinOp.OR,
        })
    
    
    def parse_expr_eager_and(self, is_stmt: bool = False) -> Node:
        """ Parse an eager and expression. """
        
        return self.parse_expr_bin(is_stmt, self.parse_expr_equality, {
            TokenType.AMPERSAND: BinOp.AND,
        })
    
    
    def parse_expr_equality(self, is_stmt: bool = False) -> Node:
        """ Parse an equality expression. """
        
        return self.parse_expr_bin(is_stmt, self.parse_expr_comparison, {
            TokenType.BANG_EQUALS: BinOp.NOT_EQUALS,
            TokenType.EQUALS_EQUALS: BinOp.EQUALS,
        })
    
    
    def parse_expr_comparison(self, is_stmt: bool = False) -> Node:
        """ Parse a comparison expression. """
        
        return self.parse_expr_bin(is_stmt, self.parse_expr_sum, {
            TokenType.LESS: BinOp.LESS,
            TokenType.LESS_EQUALS: BinOp.LESS_EQUALS,
            TokenType.GREATER: BinOp.GREATER,
            TokenType.GREATER_EQUALS: BinOp.GREATER_EQUALS,
        })
    
    
    def parse_expr_sum(self, is_stmt: bool = False) -> Node:
        """ Parse a sum expression. """
        
        return self.parse_expr_bin(is_stmt, self.parse_expr_term, {
            TokenType.PLUS: BinOp.ADD,
            TokenType.MINUS: BinOp.SUBTRACT,
        })
    
    
    def parse_expr_term(self, is_stmt: bool = False) -> Node:
        """ Parse a term expression. """
        
        return self.parse_expr_bin(is_stmt, self.parse_expr_prefix, {
            TokenType.PERCENT: BinOp.MODULO,
            TokenType.STAR: BinOp.MULTIPLY,
            TokenType.SLASH: BinOp.DIVIDE,
        })
    
    
    def parse_expr_prefix(self, is_stmt: bool = False) -> Node:
        """ Parse a prefix expression. """
        
        self.begin()
        
        OPS: dict[TokenType, UnOp] = {
            TokenType.BANG: UnOp.NOT,
            TokenType.STAR: UnOp.DEREFERENCE,
            TokenType.PLUS: UnOp.AFFIRM,
            TokenType.MINUS: UnOp.NEGATE,
        }
        
        if self.next.type in OPS:
            self.advance()
            op: UnOp = OPS[self.current.type]
            expr: Node = self.parse_expr_prefix()
            
            if not isinstance(expr, ExprNode):
                return self.abort(expr)
            
            return self.end(UnExprNode(expr, op))
        
        return self.abort(self.parse_expr_call(is_stmt))
    
    
    def parse_expr_call(self, is_stmt: bool = False) -> Node:
        """ Parse a call expression. """
        
        self.begin()
        expr: Node = self.parse_expr_primary(is_stmt)
        
        if not isinstance(expr, ExprNode):
            return self.abort(expr)
        
        while self.accept(TokenType.PARENTHESIS_OPEN):
            expr = CallExprNode(expr)
            
            if self.accept(TokenType.PARENTHESIS_CLOSE):
                self.apply(expr)
                continue
            
            param: Node = self.parse_expr()
            
            if isinstance(param, ExprNode):
                expr.params.append(param)
            else:
                self.log_error(param)
            
            while self.accept(TokenType.COMMA):
                while self.accept(TokenType.COMMA):
                    self.log_error(
                            "Missing parameter in call expression!",
                            self.current.span.end)
                
                if self.next.type == TokenType.PARENTHESIS_CLOSE:
                    self.log_error(
                            "Trailing ',' in call expression!", self.current)
                    break
                
                param = self.parse_expr()
                
                if isinstance(param, ExprNode):
                    expr.params.append(param)
                else:
                    self.log_error(param)
            
            if not self.accept(TokenType.PARENTHESIS_CLOSE):
                self.log_error(
                        "Missing closing ')' in call expression!",
                        self.current.span.end)
            
            self.apply(expr)
        
        return self.abort(expr)
    
    
    def parse_expr_primary(self, is_stmt: bool = False) -> Node:
        """ Parse a primary expression. """
        
        self.begin()
        
        if self.next.type == TokenType.PARENTHESIS_OPEN:
            return self.abort(self.parse_expr_paren())
        elif(
                self.is_parsing_std
                and self.next.type == TokenType.DOLLAR_PARENTHESIS_OPEN):
            return self.abort(self.parse_expr_intrinsic())
        elif self.accept(TokenType.LITERAL_INT):
            return self.end(IntExprNode(self.current.int_value))
        elif self.accept(TokenType.LITERAL_CHR):
            return self.end(ChrExprNode(self.current.str_value))
        elif self.accept(TokenType.LITERAL_STR):
            return self.end(StrExprNode(self.current.str_value))
        elif self.accept(TokenType.IDENTIFIER):
            return self.end(IdentifierExprNode(self.current.str_value))
        elif self.accept(TokenType.KEYWORD_FALSE):
            return self.end(IntExprNode(0))
        elif self.accept(TokenType.KEYWORD_TRUE):
            return self.end(IntExprNode(1))
        
        if is_stmt:
            self.advance()
            return self.end(ErrorNode("Expected a statement!"))
        
        node: ErrorNode = ErrorNode("Expected an expression!")
        node.span.replicate(self.current.span)
        node.span.start.replicate(node.span.end)
        return self.abort(node)
    
    
    def parse_expr_intrinsic(self) -> Node:
        """ Parse an intrinsic expression. """
        
        self.begin()
        
        if not self.accept(TokenType.DOLLAR_PARENTHESIS_OPEN):
            self.log_error(
                    "Missing opening '$(' in intrinsic expression!",
                    self.current.span.end)
        
        if not self.accept(TokenType.IDENTIFIER):
            node: ErrorNode = ErrorNode(
                    "Expected an identifier for an intrinsic name!")
            node.span.replicate(self.next.span)
            return self.abort(node)
        
        name: IdentifierExprNode = IdentifierExprNode(self.current.str_value)
        name.span.replicate(self.current.span)
        expr: IntrinsicExprNode = IntrinsicExprNode(name)
        
        while self.accept(TokenType.COMMA):
            param: Node = self.parse_expr()
            
            if not isinstance(param, ExprNode):
                self.log_error(param)
                continue
            
            expr.exprs.append(param)
        
        if not self.accept(TokenType.PARENTHESIS_CLOSE):
            self.log_error(
                    "Missing closing ')' in intrinsic expression!",
                    self.current.span.end)
        
        return self.end(expr)
