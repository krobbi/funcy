from fy_node import Node

class ErrorNode(Node):
    """ A syntax error node of an abstract syntax tree. """
    
    message: str
    """ The syntax error's message. """
    
    def __init__(self, message: str) -> None:
        """ Initialize the syntax error's message and print itself. """
        
        super().__init__()
        self.message = message
        print(self)
    
    
    def __repr__(self) -> str:
        """ Return the syntax error's string representation. """
        
        return f"Error: {self.message}"
