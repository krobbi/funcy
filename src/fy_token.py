from fy_token_type import TokenType

class Token:
    """ Information about a lexeme. """
    
    type: TokenType
    """ The token's type. """
    
    int_value: int = 0
    """ The token's integer value. """
    
    str_value: str = ""
    """ The token's string value. """
    
    def __init__(self, type: TokenType) -> None:
        """ Initialize the token's type """
        
        self.type = type
