from fy_lexer import Lexer
from fy_node import Node
from fy_node_decl_func import FuncDeclNode
from fy_node_error import ErrorNode
from fy_node_expr import ExprNode
from fy_node_expr_int import IntExprNode
from fy_node_program import ProgramNode
from fy_node_stmt import StmtNode
from fy_node_stmt_compound import CompoundStmtNode
from fy_node_stmt_expr import ExprStmtNode
from fy_node_stmt_expr_print import PrintExprStmtNode
from fy_node_stmt_nop import NopStmtNode
from fy_token import Token
from fy_token_type import TokenType

class Parser:
    """ Parses an abstract syntax tree from source code. """
    
    lexer: Lexer = Lexer()
    """ The parser's lexer. """
    
    current: Token = Token(TokenType.EOF)
    """ The currently accepted token. """
    
    next: Token = Token(TokenType.EOF)
    """ The next token to accept. """
    
    has_errors: bool = False
    """ Whether the parsed source code contained any errors. """
    
    def parse(self, source: str) -> ProgramNode:
        """ Parse an abstract syntax tree from source code. """
        
        self.lexer.begin(source)
        self.next = Token(TokenType.EOF)
        self.has_errors = False
        self.advance()
        program: ProgramNode = ProgramNode()
        
        while self.next.type != TokenType.EOF:
            func_decl: Node = self.parse_func_decl()
            
            if isinstance(func_decl, FuncDeclNode):
                program.func_decls.append(func_decl)
            else:
                self.log_error(func_decl)
        
        return program
    
    
    def log_error(self, error: str | Token | ErrorNode) -> None:
        """ Log an error object. """
        
        if isinstance(error, str):
            self.log_error(ErrorNode(error))
        elif isinstance(error, Token):
            if error.type == TokenType.ERROR:
                self.log_error(ErrorNode(error.str_value))
            else:
                print("Parser bug: Logged an error from a non-error token!")
        elif isinstance(error, ErrorNode):
            print(f"Syntax error: {error.message}")
            self.has_errors = True
        else:
            print("Parser bug: Logged an error from a non-error object!")
    
    
    def advance(self) -> None:
        """ Advance to the next token. """
        
        self.current = self.next
        self.next = self.lexer.get_token()
        
        while self.next.type == TokenType.ERROR:
            self.log_error(self.next)
            self.next = self.lexer.get_token()
    
    
    def accept(self, type: TokenType) -> bool:
        """ Accept a token. """
        
        if self.next.type == type:
            self.advance()
            return True
        else:
            return False
    
    
    def parse_func_decl(self) -> Node:
        """ Parse a function declaration. """
        
        has_func: bool = self.accept(TokenType.KEYWORD_FUNC)
        
        if not self.accept(TokenType.IDENTIFIER):
            if self.next != TokenType.KEYWORD_FUNC:
                self.advance()
            
            return ErrorNode("Expected an identifier for a function declaration's name!")
        elif not has_func:
            self.log_error("Expected 'func' for a function declaration!")
        
        func_decl: FuncDeclNode = FuncDeclNode(self.current.str_value)
        
        if not self.accept(TokenType.PARENTHESIS_OPEN):
            self.log_error(f"Missing opening '(' for {func_decl.name}'s parameter list!")
        
        if self.accept(TokenType.IDENTIFIER):
            func_decl.params.append(self.current.str_value)
            
            while self.accept(TokenType.COMMA):
                if self.accept(TokenType.IDENTIFIER):
                    func_decl.params.append(self.current.str_value)
                elif(
                        self.next.type == TokenType.PARENTHESIS_CLOSE
                        or self.next.type == TokenType.BRACE_OPEN):
                    self.log_error(f"Trailing ',' in {func_decl.name}'s parameter list!")
                    break
                else:
                    self.advance()
                    self.log_error(f"Expected an identifier for {func_decl.name}'s parameter name!")
        
        if not self.accept(TokenType.PARENTHESIS_CLOSE):
            self.log_error(f"Missing closing ')' for {func_decl.name}'s parameter list!")
        
        if self.next.type == TokenType.BRACE_OPEN:
            stmt: Node = self.parse_stmt_compound()
            
            if isinstance(stmt, CompoundStmtNode):
                func_decl.stmt = stmt
            else:
                self.log_error(stmt)
        else:
            stmt: Node = self.parse_stmt()
            
            if isinstance(stmt, StmtNode):
                self.log_error(
                        f"Expected a compound statement for {func_decl.name}'s function body!")
                compound: CompoundStmtNode = CompoundStmtNode()
                compound.stmts.append(stmt)
                func_decl.stmt = compound
            else:
                self.log_error(stmt)
        
        return func_decl
    
    
    def parse_stmt(self) -> Node:
        """ Parse a statement. """
        
        if self.next.type == TokenType.BRACE_OPEN:
            return self.parse_stmt_compound()
        elif self.accept(TokenType.SEMICOLON):
            return NopStmtNode()
        elif self.accept(TokenType.KEYWORD_PRINT):
            expr: Node = self.parse_expr(False)
            has_semicolon: bool = self.accept(TokenType.SEMICOLON)
            
            if not isinstance(expr, ExprNode):
                return expr
            elif not has_semicolon:
                self.log_error("Missing closing ';' in a print statement!")
            
            return PrintExprStmtNode(expr)
        else:
            expr: Node = self.parse_expr(True)
            has_semicolon: bool = self.accept(TokenType.SEMICOLON)
            
            if not isinstance(expr, ExprNode):
                return expr
            elif not has_semicolon:
                self.log_error("Missing closing ';' in an expression statement!")
            
            return ExprStmtNode(expr)
    
    
    def parse_stmt_compound(self) -> Node:
        """ Parse a compound statement. """
        
        if not self.accept(TokenType.BRACE_OPEN):
            self.log_error("Missing opening '{' for a compound statement!")
        
        compound_stmt: CompoundStmtNode = CompoundStmtNode()
        
        while not self.accept(TokenType.BRACE_CLOSE):
            if self.next.type == TokenType.EOF:
                self.log_error("Missing closing '}' for a compound statement!")
                break
            
            stmt: Node = self.parse_stmt()
            
            if isinstance(stmt, StmtNode):
                compound_stmt.stmts.append(stmt)
            else:
                self.log_error(stmt)
        
        return compound_stmt
    
    
    def parse_expr(self, is_stmt: bool) -> Node:
        """ Parse an expression. """
        
        return self.parse_expr_primary(is_stmt)
    
    
    def parse_expr_primary(self, is_stmt: bool) -> Node:
        """ Parse a primary expression. """
        
        if self.accept(TokenType.PARENTHESIS_OPEN):
            if self.accept(TokenType.PARENTHESIS_CLOSE):
                return ErrorNode("Missing expression in parenthesized expression!")
            
            expr: Node = self.parse_expr(is_stmt)
            has_close: bool = self.accept(TokenType.PARENTHESIS_CLOSE)
            
            if not isinstance(expr, ExprNode):
                return expr
            elif not has_close:
                self.log_error("Missing closing ')' in a parenthesized expression!")
            
            return expr
        elif self.accept(TokenType.LITERAL_INT):
            return IntExprNode(self.current.int_value)
        else:
            if is_stmt:
                self.advance()
                return ErrorNode("Expected a statement!")
            else:
                return ErrorNode("Expected an expression!")
