from fy_token import Token
from fy_token_type import TokenType

class Lexer:
    """ Generates a stream of tokens from source code. """
    
    source: str = ""
    """ The source code to read. """
    
    lexeme: str = ""
    """ The currently accepted lexeme. """
    
    character: str = ""
    """ The current character to accept. """
    
    position: int = -1
    """ The position of the current character in the source code. """
    
    BIN_DIGITS: str = "01"
    """ Binary digits. """
    
    OCT_DIGITS: str = BIN_DIGITS + "234567"
    """ Octal digits. """
    
    DEC_DIGITS: str = OCT_DIGITS + "89"
    """ Decimal digits. """
    
    HEX_DIGITS: str = DEC_DIGITS + "ABCDEFabcdef"
    """ Hexadecimal digits. """
    
    IDENTIFIER_CHARS: str = DEC_DIGITS + "ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz"
    """ Identiier characters. """
    
    def get_token(self) -> Token:
        """ Get the next token from the token stream. """
        
        while not self.is_eof():
            while self.is_whitespace() and not self.is_eof():
                self.advance()
            
            if self.character == "/" and self.peek(1) == "*":
                self.begin_token()
                self.advance(2)
                depth: int = 1
                
                while depth > 0 and not self.is_eof():
                    if self.character == "*" and self.peek(1) == "/":
                        self.advance(2)
                        depth -= 1
                    elif self.character == "/" and self.peek(1) == "*":
                        self.advance(2)
                        depth += 1
                    else:
                        self.advance()
                
                if depth > 0:
                    return self.make_error("Unterminated block comment!")
            elif self.character == "/" and self.peek(1) == "/":
                while not self.character in "\n\r" and not self.is_eof():
                    self.advance()
            else:
                break
        
        self.begin_token()
        
        if self.is_eof():
            return self.make_token(TokenType.EOF)
        elif self.consume(self.DEC_DIGITS):
            number: str = self.lexeme
            base: int = 10
            base_name: str = "decimal"
            digits: str = self.DEC_DIGITS
            
            if number == "0":
                number = ""
                
                if self.accept("Bb"):
                    base = 2
                    base_name = "binary"
                    digits = self.BIN_DIGITS
                elif self.accept("Oo"):
                    base = 8
                    base_name = "octal"
                    digits = self.OCT_DIGITS
                elif self.accept("Xx"):
                    base = 16
                    base_name = "hexadecimal"
                    digits = self.HEX_DIGITS
                else:
                    number = "0"
            
            has_trailing_underscores: bool = False
            has_adjacent_underscores: bool = False
            
            while not self.is_eof():
                if self.character in digits:
                    number += self.character
                    self.advance()
                    has_trailing_underscores = False
                elif self.accept("_"):
                    if self.consume("_"):
                        has_adjacent_underscores = True
                    
                    has_trailing_underscores = True
                else:
                    break
            
            if not number:
                return self.make_error(f"No digits in {base_name} literal!")
            elif has_trailing_underscores:
                if self.lexeme.endswith("__"):
                    return self.make_error(f"Multiple trailing '_'s in {base_name} literal!")
                else:
                    return self.make_error(f"Trailing '_' in {base_name} literal!")
            elif has_adjacent_underscores:
                return self.make_error(f"Multiple adjacent '_'s in {base_name} literal!")
            elif base == 10 and number.startswith("0") and number != "0" * len(number):
                if number.startswith("00"):
                    return self.make_error(f"Multiple leading '0's in {base_name} literal!")
                else:
                    return self.make_error(f"Leading '0' in {base_name} literal!")
            elif self.character in self.DEC_DIGITS and not self.is_eof():
                return self.make_error(f"Trailing decimal literal after {base_name} literal!")
            elif self.character in self.IDENTIFIER_CHARS and not self.is_eof():
                return self.make_error(f"Trailing identifier or keyword after {base_name} literal!")
            else:
                return self.make_int(TokenType.LITERAL_INT, int(number, base=base))
        elif self.consume(self.IDENTIFIER_CHARS):
            if self.lexeme == "func":
                return self.make_token(TokenType.KEYWORD_FUNC)
            elif self.lexeme == "print":
                return self.make_token(TokenType.KEYWORD_PRINT)
            else:
                return self.make_str(TokenType.IDENTIFIER, self.lexeme)
        elif self.accept("("):
            return self.make_token(TokenType.PARENTHESIS_OPEN)
        elif self.accept(")"):
            return self.make_token(TokenType.PARENTHESIS_CLOSE)
        elif self.accept(","):
            return self.make_token(TokenType.COMMA)
        elif self.accept(";"):
            return self.make_token(TokenType.SEMICOLON)
        elif self.accept("{"):
            return self.make_token(TokenType.BRACE_OPEN)
        elif self.accept("}"):
            return self.make_token(TokenType.BRACE_CLOSE)
        
        if self.lexeme:
            return self.make_error(f"Lexer bug: Fell through after accepting '{self.lexeme}'")
        else:
            self.advance()
            return self.make_error(f"Illegal character '{self.lexeme}'!")
    
    
    def is_eof(self) -> bool:
        """ Get whether the current position is out of bounds. """
        
        return self.position < 0 or self.position >= len(self.source)
    
    
    def is_whitespace(self) -> bool:
        """ Get whether the current character is a whitespace character. """
        
        return len(self.character) != 1 or ord(self.character) <= 32
    
    
    def begin(self, source: str) -> None:
        """ Begin the lexer from source code. """
        
        self.source = source
        self.position = -1
        self.advance()
        self.begin_token()
    
    
    def begin_token(self) -> None:
        """ Mark the current position as the start of a new token. """
        
        self.lexeme = ""
    
    
    def peek(self, offset: int) -> str:
        """ Return the character at an offset from the current position. """
        
        peek_position: int = self.position + offset
        
        if peek_position >= 0 and peek_position < len(self.source):
            return self.source[peek_position]
        else:
            return ""
    
    
    def advance(self, amount: int = 1) -> None:
        """ Advance the current position by an amount. """
        
        for i in range(amount):
            self.lexeme += self.character
            self.position += 1
            self.character = self.peek(0)
    
    
    def accept(self, characters: str) -> bool:
        """ Accept a character from a set of characters. """
        
        if self.character in characters and not self.is_eof():
            self.advance()
            return True
        else:
            return False
    
    
    def consume(self, characters: str) -> bool:
        """ Accept a sequence of characters from a set of characters. """
        if self.character in characters and not self.is_eof():
            while self.character in characters and not self.is_eof():
                self.advance()
            
            return True
        else:
            return False
    
    
    def make_token(self, type: TokenType) -> Token:
        """ Make a token from its type. """
        
        return Token(type)
    
    
    def make_error(self, message: str) -> Token:
        """ Make a syntax error token from its message. """
        
        return self.make_str(TokenType.ERROR, message)
    
    
    def make_int(self, type: TokenType, value: int) -> Token:
        """ Make an integer token from its type and value. """
        
        token: Token = self.make_token(type)
        token.int_value = value
        return token
    
    
    def make_str(self, type: TokenType, value: str) -> Token:
        """ Make a string token from its type and value. """
        
        token: Token = self.make_token(type)
        token.str_value = value
        return token
