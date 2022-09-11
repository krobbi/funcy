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
    
    def parse(self, source: str) -> ProgramNode:
        """ Parse an abstract syntax tree from source code. """
        
        self.lexer.begin(source)
        self.next = Token(TokenType.EOF)
        self.advance()
        program: ProgramNode = ProgramNode()
        
        while self.next.type != TokenType.EOF:
            func_decl: Node = self.parse_func_decl()
            
            if isinstance(func_decl, FuncDeclNode):
                program.func_decls.append(func_decl)
        
        return program
    
    
    def advance(self) -> None:
        """ Advance to the next token. """
        
        self.current = self.next
        self.next = self.lexer.get_token()
        
        while self.next.type == TokenType.ERROR:
            print(f"Error: {self.next.str_value}")
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
        
        if not self.accept(TokenType.KEYWORD_FUNC):
            self.advance()
            return ErrorNode("Expected 'func' for a function declaration!")
        elif not self.accept(TokenType.IDENTIFIER):
            return ErrorNode("Expected an identifer for a function declaration's name!")
        
        func_decl: FuncDeclNode = FuncDeclNode(self.current.str_value)
        
        if not self.accept(TokenType.PARENTHESIS_OPEN):
            return ErrorNode(f"Missing opening '(' for {func_decl.name}'s parameter list!")
        elif self.accept(TokenType.IDENTIFIER):
            func_decl.params.append(self.current.str_value)
            
            while self.accept(TokenType.COMMA):
                if self.accept(TokenType.IDENTIFIER):
                    func_decl.params.append(self.current.str_value)
                else:
                    return ErrorNode(
                            f"Expected an identifier for {func_decl.name}'s parameter name!")
        
        if not self.accept(TokenType.PARENTHESIS_CLOSE):
            return ErrorNode(f"Missing closing ')' for {func_decl.name}'s parameter list!")
        
        stmt: Node = self.parse_stmt_compound()
        
        if isinstance(stmt, CompoundStmtNode):
            func_decl.stmt = stmt
            return func_decl
        else:
            return stmt
    
    
    def parse_stmt(self) -> Node:
        """ Parse a statement. """
        
        if self.next.type == TokenType.BRACE_OPEN:
            return self.parse_stmt_compound()
        elif self.accept(TokenType.SEMICOLON):
            return NopStmtNode()
        elif self.accept(TokenType.KEYWORD_PRINT):
            expr: Node = self.parse_expr()
            
            if not isinstance(expr, ExprNode):
                return expr
            elif self.accept(TokenType.SEMICOLON):
                return PrintExprStmtNode(expr)
            else:
                return ErrorNode("Missing closing ';' in a print statement!")
        else:
            expr: Node = self.parse_expr()
            
            if not isinstance(expr, ExprNode):
                return expr
            elif self.accept(TokenType.SEMICOLON):
                return ExprStmtNode(expr)
            else:
                return ErrorNode("Missing closing ';' in an expression statement!")
    
    
    def parse_stmt_compound(self) -> Node:
        """ Parse a compound statement. """
        
        if not self.accept(TokenType.BRACE_OPEN):
            return ErrorNode("Missing opening '{' for a compound statement!")
        
        compound_stmt: CompoundStmtNode = CompoundStmtNode()
        
        while not self.accept(TokenType.BRACE_CLOSE):
            if self.next.type == TokenType.EOF:
                return ErrorNode("Missing closing '}' for a compound statement!")
            
            stmt: Node = self.parse_stmt()
            
            if isinstance(stmt, StmtNode):
                compound_stmt.stmts.append(stmt)
            else:
                return stmt
        
        return compound_stmt
    
    
    def parse_expr(self) -> Node:
        """ Parse an expression. """
        
        return self.parse_expr_primary()
    
    
    def parse_expr_primary(self) -> Node:
        """ Parse a primary expression. """
        
        if self.accept(TokenType.PARENTHESIS_OPEN):
            expr: Node = self.parse_expr()
            
            if not isinstance(expr, ExprNode) or self.accept(TokenType.PARENTHESIS_CLOSE):
                return expr
            else:
                return ErrorNode("Missing closing ')' in a parenthesized expression!")
        elif self.accept(TokenType.LITERAL_INT):
            return IntExprNode(self.current.int_value)
        else:
            return ErrorNode("Expected a statement!")
