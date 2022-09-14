from fy_ir_op import IROp

class IRBlock:
    """ A labeled IR block. """
    
    label: str
    """ The IR block's label. """
    
    ops: list[IROp]
    """ The IR block's IR operations. """
    
    def __init__(self, label: str) -> None:
        """ Initialize the IR block's label and IR operations. """
        
        self.label = label
        self.ops = []
    
    
    def __repr__(self) -> str:
        """ Return the IR block's string representation. """
        
        return f"{self.label}:"
