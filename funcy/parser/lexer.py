from .position import Span
from .token import Token, TokenType

class Lexer:
    """ Generates a stream of tokens from source code. """
    
    TAB_SIZE: int = 4
    """ The size of a tab character in columns. """
    
    BIN_DIGITS: str = "01"
    """ Binary digits. """
    
    OCT_DIGITS: str = BIN_DIGITS + "234567"
    """ Octal digits. """
    
    DEC_DIGITS: str = OCT_DIGITS + "89"
    """ Decimal digits. """
    
    HEX_DIGITS: str = DEC_DIGITS + "ABCDEFabcdef"
    """ Hexadecimal digits. """
    
    IDENTIFIER_CHARS: str = (
            DEC_DIGITS
            + "ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz")
    
    source: str = ""
    """ The source code to read. """
    
    character: str = ""
    """ The next character to accept. """
    
    span: Span = Span()
    """ The next token's span. """
    
    lexeme: str = ""
    """ The next token's lexeme. """
    
    def get_token(self) -> Token:
        """ Get the next token from the token stream. """
        
        while self.character:
            while self.character and ord(self.character) <= 32:
                self.advance()
            
            if self.character == "/" and self.peek(1) == "*":
                self.begin_token()
                self.advance(2)
                depth: int = 1
                
                while self.character and depth > 0:
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
                while self.character and not self.character in "\n\r":
                    self.advance()
            else:
                break
        
        self.begin_token()
        
        if not self.character:
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
            
            while self.character:
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
                    return self.make_error(
                            f"Multiple trailing '_'s in {base_name} literal!")
                else:
                    return self.make_error(
                            f"Trailing '_' in {base_name} literal!")
            elif has_adjacent_underscores:
                return self.make_error(
                        f"Multiple adjacent '_'s in {base_name} literal!")
            elif(
                    base == 10 and number.startswith("0")
                    and number != "0" * len(number)):
                if number.startswith("00"):
                    return self.make_error(
                            f"Multiple leading '0's in {base_name} literal!")
                else:
                    return self.make_error(
                            f"Leading '0' in {base_name} literal!")
            elif self.character and self.character in self.DEC_DIGITS:
                return self.make_error(
                        f"Trailing decimal literal after {base_name} literal!")
            elif self.character and self.character in self.IDENTIFIER_CHARS:
                return self.make_error(
                        "Trailing identifier or keyword "
                        f"after {base_name} literal!")
            
            return self.make_int(TokenType.LITERAL_INT, int(number, base=base))
        elif self.consume(self.IDENTIFIER_CHARS):
            if self.lexeme == "func":
                return self.make_token(TokenType.KEYWORD_FUNC)
            elif self.lexeme == "print":
                return self.make_token(TokenType.KEYWORD_PRINT)
            elif self.lexeme == "return":
                return self.make_token(TokenType.KEYWORD_RETURN)
            else:
                return self.make_str(TokenType.IDENTIFIER, self.lexeme)
        elif self.accept("%"):
            return self.make_token(TokenType.PERCENT)
        elif self.accept("("):
            return self.make_token(TokenType.PARENTHESIS_OPEN)
        elif self.accept(")"):
            return self.make_token(TokenType.PARENTHESIS_CLOSE)
        elif self.accept("*"):
            return self.make_token(TokenType.STAR)
        elif self.accept("+"):
            return self.make_token(TokenType.PLUS)
        elif self.accept(","):
            return self.make_token(TokenType.COMMA)
        elif self.accept("-"):
            return self.make_token(TokenType.MINUS)
        elif self.accept("/"):
            return self.make_token(TokenType.SLASH)
        elif self.accept(";"):
            return self.make_token(TokenType.SEMICOLON)
        elif self.accept("{"):
            return self.make_token(TokenType.BRACE_OPEN)
        elif self.accept("}"):
            return self.make_token(TokenType.BRACE_CLOSE)
        
        if self.lexeme:
            return self.make_error(
                    f"Bug: Fell through after accepting '{self.lexeme}'!")
        
        self.advance()
        return self.make_error(f"Illegal character '{self.lexeme}'!")
    
    
    def begin(self, source: str) -> None:
        """ Begin the lexer from source code. """
        
        self.source = source
        self.span.reset()
        self.begin_token()
        self.character = self.peek(0)
    
    
    def begin_token(self) -> None:
        """ Mark the current position as the start of a token. """
        
        self.span.begin()
        self.lexeme = ""
    
    
    def peek(self, offset: int) -> str:
        """ Peek the character at an offset from the next token. """
        
        peek_offset: int = self.span.end.offset + offset
        
        if peek_offset < 0 or peek_offset >= len(self.source):
            return ""
        
        return self.source[peek_offset]
    
    
    def advance(self, amount: int = 1) -> None:
        """ Advance the current position by an amount of characters. """
        
        for i in range(amount):
            self.span.advance(self.character, self.TAB_SIZE)
            self.lexeme += self.character
            self.character = self.peek(0)
    
    
    def accept(self, characters: str) -> bool:
        """ Accept the next character from a set of characters. """
        
        if not self.character or not self.character in characters:
            return False
        
        self.advance()
        return True
    
    
    def consume(self, characters: str) -> bool:
        """ Consume characters from a set of characters. """
        
        if not self.character or not self.character in characters:
            return False
        
        while self.character and self.character in characters:
            self.advance()
        
        return True
    
    
    def make_token(self, type: TokenType) -> Token:
        """ Make a token from its type. """
        
        return Token(type, self.span.copy(), self.lexeme)
    
    
    def make_error(self, message: str) -> Token:
        """ Make a syntax error from its message. """
        
        return self.make_str(TokenType.ERROR, message)
    
    
    def make_int(self, type: TokenType, value: int) -> Token:
        """ Make an integer token from its type and value. """
        
        result: Token = self.make_token(type)
        result.int_value = value
        return result
    
    
    def make_str(self, type: TokenType, value: str) -> Token:
        """ Make a string token from its type and value. """
        
        result: Token = self.make_token(type)
        result.str_value = value
        return result
