from msilib.schema import AdvtExecuteSequence
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
    
    KEYWORDS: dict[str, TokenType] = {
        "break": TokenType.KEYWORD_BREAK,
        "continue": TokenType.KEYWORD_CONTINUE,
        "else": TokenType.KEYWORD_ELSE,
        "false": TokenType.KEYWORD_FALSE,
        "func": TokenType.KEYWORD_FUNC,
        "if": TokenType.KEYWORD_IF,
        "include": TokenType.KEYWORD_INCLUDE,
        "let": TokenType.KEYWORD_LET,
        "mut": TokenType.KEYWORD_MUT,
        "return": TokenType.KEYWORD_RETURN,
        "true": TokenType.KEYWORD_TRUE,
        "while": TokenType.KEYWORD_WHILE,
        "!": TokenType.BANG,
        "!=": TokenType.BANG_EQUALS,
        "%": TokenType.PERCENT,
        "%=": TokenType.PERCENT_EQUALS,
        "&": TokenType.AMPERSAND,
        "&&": TokenType.AMPERSAND_AMPERSAND,
        "&=": TokenType.AMPERSAND_EQUALS,
        "(": TokenType.PARENTHESIS_OPEN,
        ")": TokenType.PARENTHESIS_CLOSE,
        "*": TokenType.STAR,
        "*=": TokenType.STAR_EQUALS,
        "+": TokenType.PLUS,
        "+=": TokenType.PLUS_EQUALS,
        ",": TokenType.COMMA,
        "-": TokenType.MINUS,
        "-=": TokenType.MINUS_EQUALS,
        "/": TokenType.SLASH,
        "/=": TokenType.SLASH_EQUALS,
        ";": TokenType.SEMICOLON,
        "<": TokenType.LESS,
        "<=": TokenType.LESS_EQUALS,
        "=": TokenType.EQUALS,
        "==": TokenType.EQUALS_EQUALS,
        ">": TokenType.GREATER,
        ">=": TokenType.GREATER_EQUALS,
        "{": TokenType.BRACE_OPEN,
        "|": TokenType.PIPE,
        "|=": TokenType.PIPE_EQUALS,
        "||": TokenType.PIPE_PIPE,
        "}": TokenType.BRACE_CLOSE,
    }
    """ Token types with fixed lexemes and no value. """
    
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
        elif self.accept("\"'"):
            terminator: str = self.lexeme
            is_chr: bool = terminator == "'"
            has_seen_terminator: bool = False
            value: str = ""
            
            while self.character:
                if self.accept(terminator):
                    has_seen_terminator = True
                    break
                elif self.accept("\n\r"):
                    break
                elif self.accept("\\"):
                    if self.character == "\r":
                        self.advance() # Allow '\r\n' sequences.
                    
                    if self.accept("Aa"):
                        value += "\a"
                    elif self.accept("Bb"):
                        value += "\b"
                    elif self.accept("Ff"):
                        value += "\f"
                    elif self.accept("Nn"):
                        value += "\n"
                    elif self.accept("Rr"):
                        value += "\r"
                    elif self.accept("Vv"):
                        value += "\v"
                    elif self.accept("Xx"):
                        if(
                                not self.character in self.HEX_DIGITS
                                or not self.peek(1) in self.HEX_DIGITS):
                            return self.make_error(
                                    "Missing 2 digit hexadecimal "
                                    "number in \\x escape sequence!")
                        
                        number: str = self.character + self.peek(1)
                        self.advance(2)
                        value += chr(int(number, base=16))
                    elif not self.accept("\n"):
                        value += self.character
                        self.advance()
                else:
                    value += self.character
                    self.advance()
            
            if not has_seen_terminator:
                if is_chr:
                    return self.make_error("Unterminated character literal!")
                
                return self.make_error("Unterminated string literal!")
            
            if is_chr:
                return self.make_str(TokenType.LITERAL_CHR, value)
            
            return self.make_str(TokenType.LITERAL_STR, value)
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
            if self.lexeme in self.KEYWORDS:
                return self.make_token(self.KEYWORDS[self.lexeme])
            
            return self.make_str(TokenType.IDENTIFIER, self.lexeme)
        elif self.character == "$" and self.peek(1) == "(":
            self.advance(2)
            return self.make_token(TokenType.DOLLAR_PARENTHESIS_OPEN)
        else:
            position: int = self.span.start.offset
            max_length: int = max(len(key) for key in self.KEYWORDS)
            max_length = min(max_length, len(self.source) - position)
            
            for length in range(max_length, 0, -1):
                keyword: str = self.source[position:position + length]
                
                if keyword in self.KEYWORDS:
                    self.advance(length)
                    return self.make_token(self.KEYWORDS[keyword])
        
        if self.lexeme:
            return self.make_error(
                    f"Bug: Fell through after accepting '{self.lexeme}'!")
        
        self.advance()
        matches: list[str] = []
        
        for keyword in self.KEYWORDS:
            if keyword.startswith(self.lexeme):
                matches.append(keyword)
        
        if matches:
            message: str = f"No token named '{self.lexeme}'! Did you mean "
            
            for i, v in enumerate(matches):
                message += f"'{v}'"
                
                if i < len(matches) - 1:
                    if len(matches) > 2:
                        message += ","
                    
                    message += " "
                
                if i == len(matches) - 2:
                    message += "or "
            
            return self.make_error(f"{message}?")
        
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
        
        return Token(type, self.span.copy())
    
    
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
