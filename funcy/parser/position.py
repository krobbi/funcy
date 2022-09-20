class Position:
    """ A position in text. """
    
    offset: int
    """ The position's offset in characters into the text. """
    
    line: int
    """ The position's line in the text. """
    
    column: int
    """ The position's column in the text. """
    
    def __init__(self) -> None:
        """ Initialize the position's position. """
        
        self.reset()
    
    
    def __str__(self) -> str:
        """ Return the position's string. """
        
        return f"{self.line}:{self.column}"
    
    
    def reset(self) -> None:
        """ Reset the position to the start of the text. """
        
        self.offset = 0
        self.line = 1
        self.column = 1
    
    
    def advance(self, text: str, tab_size: int) -> None:
        """ Advance the position by a string of text. """
        
        for character in text:
            self.offset += 1
            
            if character == "\t":
                self.column += tab_size - (self.column - 1) % tab_size
            elif character == "\n":
                self.column = 1
                self.line += 1
            elif character == "\r":
                self.column = 1
            else:
                self.column += 1
    
    
    def replicate(self, other) -> None:
        """ Replicate another position by value. """
        
        self.offset = other.offset
        self.line = other.line
        self.column = other.column


class Span:
    """ A span between two positions in text. """
    
    start: Position
    """ The span's start position. """
    
    end: Position
    """ The span's end position. """
    
    def __init__(self) -> None:
        """ Initialize the span's positions. """
        
        self.start = Position()
        self.end = Position()
    
    
    def __str__(self) -> str:
        """ Return the span's string. """
        
        if len(self) <= 1:
            return str(self.start)
        elif self.start.line == self.end.line:
            return f"{self.start}-{self.end.column}"
        
        return f"{self.start} - {self.end}"
    
    
    def __len__(self) -> int:
        """ Return the span's length. """
        
        return self.end.offset - self.start.offset
    
    
    def reset(self) -> None:
        """ Reset the span to the start of the text. """
        
        self.start.reset()
        self.end.reset()
    
    
    def begin(self) -> None:
        """ Move the span's start position to its end position. """
        
        self.start.replicate(self.end)
    
    
    def advance(self, text: str, tab_size: int) -> None:
        """ Advance the span's end position by a string of text. """
        
        self.end.advance(text, tab_size)
    
    
    def copy(self):
        """ Create a copy of the span by value. """
        
        result: Span = Span()
        result.end.replicate(self.end)
        result.start.replicate(self.start)
        return result
