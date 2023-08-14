from enum import Enum, auto

from .position import Span

class TokenType(Enum):
    """ The type of a token. """
    
    EOF = auto()
    """ End of file marker. """
    
    ERROR = auto()
    """ Syntax error. (Skipped by parser.) """
    
    LITERAL_INT = auto()
    """ Integer value. """
    
    LITERAL_CHR = auto()
    """ Character value. """
    
    LITERAL_STR = auto()
    """ String value. """
    
    IDENTIFIER = auto()
    """ User-defined name. """
    
    KEYWORD_BREAK = auto()
    """ `break`. """
    
    KEYWORD_CONTINUE = auto()
    """ `continue`. """
    
    KEYWORD_ELSE = auto()
    """ `else`. """
    
    KEYWORD_FALSE = auto()
    """ `false`. """
    
    KEYWORD_FUNC = auto()
    """ `func`. """
    
    KEYWORD_IF = auto()
    """ `if`. """
    
    KEYWORD_INCLUDE = auto()
    """ `include`. """
    
    KEYWORD_LET = auto()
    """ `let`. """
    
    KEYWORD_MUT = auto()
    """ `mut`. """
    
    KEYWORD_RETURN = auto()
    """ `return`. """
    
    KEYWORD_TRUE = auto()
    """ `true`. """
    
    KEYWORD_WHILE = auto()
    """ `while`. """
    
    BANG = auto()
    """ `!`. """
    
    BANG_EQUALS = auto()
    """ `!=`. """
    
    PERCENT = auto()
    """ `%`. """
    
    PERCENT_EQUALS = auto()
    """ `%=`. """
    
    AMPERSAND = auto()
    """ `&`. """
    
    AMPERSAND_AMPERSAND = auto()
    """ `&&`. """
    
    AMPERSAND_EQUALS = auto()
    """ `&=`. """
    
    PARENTHESIS_OPEN = auto()
    """ `(`. """
    
    PARENTHESIS_CLOSE = auto()
    """ `)`. """
    
    STAR = auto()
    """ `*`. """
    
    STAR_EQUALS = auto()
    """ `*=`. """
    
    PLUS = auto()
    """ `+`. """
    
    PLUS_EQUALS  = auto()
    """ `+=`. """
    
    COMMA = auto()
    """ `,`. """
    
    MINUS = auto()
    """ `-`. """
    
    MINUS_EQUALS = auto()
    """ `-=`. """
    
    SLASH = auto()
    """ `/`. """
    
    SLASH_EQUALS = auto()
    """ `/=`. """
    
    SEMICOLON = auto()
    """ `;`. """
    
    LESS = auto()
    """ `<`. """
    
    LESS_EQUALS = auto()
    """ `<=`. """
    
    EQUALS = auto()
    """ `=`. """
    
    EQUALS_EQUALS = auto()
    """ `==`. """
    
    GREATER = auto()
    """ `>` """
    
    GREATER_EQUALS = auto()
    """ `>=`. """
    
    BRACE_OPEN = auto()
    """ `{`. """
    
    PIPE = auto()
    """ `|`. """
    
    PIPE_EQUALS = auto()
    """ `|=`. """
    
    PIPE_PIPE = auto()
    """ `||`. """
    
    BRACE_CLOSE = auto()
    """ `}`. """


class Token:
    """ Information about a lexeme. """
    
    type: TokenType
    """ The token's type. """
    
    span: Span
    """ The token's span. """
    
    int_value: int = 0
    """ The token's integer value. """
    
    str_value: str = ""
    """ The token's string value. """
    
    def __init__(self, type: TokenType, span: Span) -> None:
        """ Initialize the token's type and span. """
        
        self.type = type
        self.span = span
    
    
    def __str__(self) -> str:
        """ Return the token's string. """
        
        result: str = f"{self.span}: {self.type.name}"
        
        if self.type in (
                TokenType.ERROR, TokenType.LITERAL_CHR,
                TokenType.LITERAL_STR, TokenType.IDENTIFIER):
            result += f": {self.str_value}"
        elif self.type == TokenType.LITERAL_INT:
            result += f": {self.int_value}"
        
        return result
