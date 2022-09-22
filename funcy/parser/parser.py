from ..ast.nodes import *
from ..io.log import Log
from .lexer import Lexer
from .position import Position, Span
from .token import Token, TokenType

class Parser:
    """ Parses an abstract syntax tree from source code. """
    
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
        self.next = Token(TokenType.EOF, Span(), "")
        self.current = Token(TokenType.EOF, Span(), "")
        self.span_stack = []
    
    
    def parse(self, source: str) -> RootNode:
        """ Parse an abstract syntax tree from source code. """
        
        self.lexer.begin(source)
        self.next = Token(TokenType.EOF, Span(), "")
        self.advance()
        self.span_stack = []
        
        self.begin()
        root: RootNode = RootNode()
        
        while self.next.type != TokenType.EOF:
            stmt: Node = self.parse_stmt_func()
            
            if not isinstance(stmt, FuncStmtNode):
                self.log_error(stmt)
                continue
            
            root.stmts.append(stmt)
        
        return self.end(root)
    
    
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
    
    
    def end(self, node: Node) -> Node:
        """ End a node's position at the current token. """
        
        node.span.replicate(self.span_stack.pop())
        node.span.include(self.current.span)
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
        elif self.accept(TokenType.SEMICOLON):
            return self.end(NopStmtNode())
        elif self.accept(TokenType.KEYWORD_PRINT):
            expr: Node = self.parse_expr_paren()
            has_semicolon: bool = self.accept(TokenType.SEMICOLON)
            
            if not isinstance(expr, ExprNode):
                return self.abort(expr)
            
            if not has_semicolon:
                self.log_error(
                        "Missing closing ';' in print statement!",
                        self.current.span.end)
            
            return self.end(PrintStmtNode(expr))
        
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
        has_func: bool = self.accept(TokenType.KEYWORD_FUNC)
        
        if not has_func:
            self.log_error(
                    "Missing 'func' in function statement!",
                    self.next.span.start)
        
        if not self.accept(TokenType.IDENTIFIER):
            node: ErrorNode = ErrorNode(
                    "Expected an identifier for a function name!")
            node.span.replicate(self.next.span)
            
            if not has_func:
                self.advance()
            
            return self.abort(node)
        
        name: IdentifierExprNode = IdentifierExprNode(self.current.str_value)
        name.span.replicate(self.current.span)
        params: list[IdentifierExprNode] = []
        
        if not self.accept(TokenType.PARENTHESIS_OPEN):
            self.log_error(
                    f"Missing opening '(' in {name.name}'s parameter list!",
                    self.current.span.end)
        
        if self.accept(TokenType.IDENTIFIER):
            param: IdentifierExprNode = IdentifierExprNode(
                    self.current.str_value)
            param.span.replicate(self.current.span)
            params.append(param)
            
            if self.next.type == TokenType.IDENTIFIER:
                self.log_error(
                        f"Missing ',' after {name.name}'s {params[0].name} "
                        "parameter!", self.current.span.end)
            
            while(
                    self.accept(TokenType.COMMA)
                    or self.next.type == TokenType.IDENTIFIER):
                while self.accept(TokenType.COMMA):
                    self.log_error(
                            f"Missing parameter in {name.name}'s "
                            "parameter list!", self.current.span.start)
                
                if not self.accept(TokenType.IDENTIFIER):
                    self.log_error(
                            f"Trailing ',' in {name.name}'s parameter list!",
                            self.current)
                    break
                
                param = IdentifierExprNode(self.current.str_value)
                param.span.replicate(self.current.span)
                params.append(param)
                
                while self.next.type == TokenType.IDENTIFIER:
                    self.log_error(
                            f"Missing ',' after {name.name}'s "
                            f"{params[-1].name} parameter!",
                            self.current.span.end)
                    self.advance()
                    param = IdentifierExprNode(self.current.str_value)
                    param.span.replicate(self.current.span)
                    params.append(param)
        
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
            return self.end(FuncStmtNode(name, params, stmt))
        
        stmt: Node = self.parse_stmt_block()
        
        if not isinstance(stmt, StmtNode):
            return self.abort(stmt)
        
        return self.end(FuncStmtNode(name, params, stmt))
    
    
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
        
        if not isinstance(expr, ExprNode):
            return self.abort(expr)
        
        return self.end(expr)
    
    
    def parse_expr(self, is_stmt: bool = False) -> Node:
        """ Parse an expression. """
        
        self.begin()
        expr: Node = self.parse_expr_primary(is_stmt)
        
        if not isinstance(expr, ExprNode):
            return self.abort(expr)
        
        return self.end(expr)
    
    
    def parse_expr_primary(self, is_stmt: bool) -> Node:
        """ Parse a primary expression. """
        
        self.begin()
        
        if self.next.type == TokenType.PARENTHESIS_OPEN:
            return self.end(self.parse_expr_paren())
        elif self.accept(TokenType.LITERAL_INT):
            return self.end(IntExprNode(self.current.int_value))
        elif self.accept(TokenType.IDENTIFIER):
            return self.end(IdentifierExprNode(self.current.str_value))
        
        if is_stmt:
            self.advance()
            return self.end(ErrorNode("Expected a statement!"))
        
        node: ErrorNode = ErrorNode("Expected an expression!")
        node.span.replicate(self.current.span)
        node.span.start.replicate(node.span.end)
        return self.abort(node)
