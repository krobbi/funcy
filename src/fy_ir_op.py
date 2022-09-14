from fy_ir_op_type import IROpType

class IROp:
    """ An IR operation. """
    
    type: IROpType
    """ The IR operation's type. """
    
    int_value: int = 0
    """ The IR operation's integer value. """
    
    str_value: str = ""
    """ The IR operation's string value. """
    
    def __init__(self, type: IROpType) -> None:
        """ Initialize the IR operation's type. """
        
        self.type = type
    
    
    def __repr__(self) -> str:
        """ Return the IR operation's string representation. """
        
        if self.type == IROpType.CALL_ARGC or self.type == IROpType.PUSH_INT:
            return f"{self.type.name} {self.int_value};"
        elif self.type == IROpType.BRANCH_ALWAYS_LABEL or self.type == IROpType.PUSH_LABEL:
            return f"{self.type.name} {self.str_value};"
        else:
            return f"{self.type.name};"
