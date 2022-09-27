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
    
    IDENTIFIER = auto()
    """ User-defined name. """
    
    KEYWORD_FUNC = auto()
    """ `func`. """
    
    KEYWORD_PRINT = auto()
    """ `print`. """
    
    KEYWORD_RETURN = auto()
    """ `return`. """
    
    PERCENT = auto()
    """ `%`. """
    
    PARENTHESIS_OPEN = auto()
    """ `(`. """
    
    PARENTHESIS_CLOSE = auto()
    """ `)`. """
    
    STAR = auto()
    """ `*`. """
    
    PLUS = auto()
    """ `+`. """
    
    COMMA = auto()
    """ `,`. """
    
    MINUS = auto()
    """ `-`. """
    
    SLASH = auto()
    """ `/`. """
    
    SEMICOLON = auto()
    """ `;`. """
    
    BRACE_OPEN = auto()
    """ `{`. """
    
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
        
        if self.type == TokenType.ERROR or self.type == TokenType.IDENTIFIER:
            result += f": {self.str_value}"
        elif self.type == TokenType.LITERAL_INT:
            result += f": {self.int_value}"
        
        return result
