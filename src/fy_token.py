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
    
    
    def __repr__(self) -> str:
        """ Return the token's string representation. """
        
        if self.type == TokenType.ERROR or self.type == TokenType.IDENTIFIER:
            return f"{self.type.name}: {self.str_value}"
        elif self.type == TokenType.LITERAL_INT:
            return f"{self.type.name}: {self.int_value}"
        else:
            return self.type.name
