from enum import Enum, auto

class TokenType(Enum):
    """ The type of a token. """
    
    ERROR = auto()
    """ Syntax error. """
    
    EOF = auto()
    """ End of file. """
    
    LITERAL_INT = auto()
    """ Integer value. """
    
    IDENTIFIER = auto()
    """ User-defined name. """
    
    KEYWORD_FUNC = auto()
    """ `func`. """
    
    KEYWORD_PRINT = auto()
    """ `print`. """
    
    PARENTHESIS_OPEN = auto()
    """ `(`. """
    
    PARENTHESIS_CLOSE = auto()
    """ `)`. """
    
    COMMA = auto()
    """ `,`. """
    
    SEMICOLON = auto()
    """ `;`. """
    
    BRACE_OPEN = auto()
    """ `{`. """
    
    BRACE_CLOSE = auto()
    """ `}`. """
