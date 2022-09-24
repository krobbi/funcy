from ..fvm import FVM

class InputWrapper:
    """ Wraps code input to the Funcy SDK. """
    
    path: str
    """ The input's path. """
    
    is_ok: bool
    """ Whether the input was read successfully. """
    
    is_binary: bool
    """ Whether the input is binary. """
    
    source: str
    """ The input's source code. """
    
    bytecode: bytes
    """ The input's bytecode. """
    
    def __init__(self) -> None:
        """ Initialize the input wrapper's data. """
        
        self.clear()
    
    
    def clear(self) -> None:
        """ Clear the input wrapper. """
        
        self.path = ""
        self.is_ok = True
        self.is_binary = False
        self.source = ""
        self.bytecode = bytes([])
    
    
    def from_source(self, source: str) -> None:
        """ Load the input wrapper from source code. """
        
        self.clear()
        self.source = source
    
    
    def from_path(self, path: str) -> None:
        """ Load the input wrapper from a path. """
        
        self.clear()
        self.path = path
        
        try:
            with open(path, "rb") as file:
                self.bytecode = file.read(len(FVM.HEADER))
                
                if self.bytecode == FVM.HEADER:
                    self.is_binary = True
                    self.bytecode = self.bytecode + file.read()
            
            if self.is_binary:
                return
            
            self.bytecode = bytes([])
            
            with open(path, "rt") as file:
                self.source = file.read()
        except IOError:
            self.is_ok = False
