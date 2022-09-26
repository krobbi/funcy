from enum import Enum, auto

class OpType(Enum):
    """ The type of an IR operation. """
    
    HALT = auto()
    """ Pop and halt element. """
    
    CALL_PARAMC = auto()
    """ Call with parameter count. """
    
    RETURN = auto()
    """ Pop and return element. """
    
    PUSH_LABEL = auto()
    """ Push labeled address. """
    
    PUSH_INT = auto()
    """ Push integer value. """
    
    DROP = auto()
    """ Pop and discard element. """
    
    PRINT = auto()
    """ Pop and print element. """


class Op:
    """ An IR operation. """
    
    type: OpType
    """ The IR operation's type. """
    
    int_value: int = 0
    """ The IR operation's integer value. """
    
    str_value: str = ""
    """ The IR operation's string value. """
    
    def __init__(self, type: OpType) -> None:
        """ Initialize the IR operation's type. """
        
        self.type = type
    
    
    def __str__(self) -> str:
        """ Return the IR operation's string. """
        
        if self.type == OpType.CALL_PARAMC or self.type == OpType.PUSH_INT:
            return f"{self.type.name} {self.int_value};"
        elif self.type == OpType.PUSH_LABEL:
            return f"{self.type.name} {self.str_value};"
        else:
            return f"{self.type.name};"


class Block:
    """ A labeled block of IR code. """
    
    label: str
    """ The IR block's label. """
    
    ops: list[Op]
    """ The IR block's IR operations. """
    
    def __init__(self, label: str) -> None:
        """ Initialize the IR block's label and IR operations. """
        
        self.label = label
        self.ops = []
    
    
    def __str__(self) -> str:
        """ Return the block's string. """
        
        return f"{self.label}:"


class Code:
    """ An IR code program. """
    
    label_count: int
    """ The IR code's label count. """
    
    blocks: list[Block]
    """ The IR code's blocks. """
    
    current: Block
    """ The IR code's current block. """
    
    def __init__(self) -> None:
        """ Initialize the IR code. """
        
        self.clear()
    
    
    def clear(self) -> None:
        """ Clear the IR code. """
        
        self.current = Block(".main")
        self.blocks = [self.current]
        self.label_count = 0
    
    
    def get_label(self) -> str:
        """ Get the current label. """
        
        return self.current.label
    
    
    def set_label(self, label: str) -> None:
        """ Set the current label. """
        
        for block in self.blocks:
            if block.label == label:
                self.current = block
                return
    
    
    def append_label(self, name: str) -> str:
        """ Append a label at the end of the IR code. """
        
        self.label_count += 1
        label: str = f".L{self.label_count}_{name}"
        self.blocks.append(Block(label))
        return label
    
    
    def make_halt(self) -> None:
        """ Make a halt IR operation. """
        
        self.append_op_standalone(OpType.HALT)
    
    
    def make_call_paramc(self, paramc: int) -> None:
        """ Make a call paramc IR operation. """
        
        self.append_op_int(OpType.CALL_PARAMC, paramc)
    
    
    def make_return(self) -> None:
        """ Make a return IR operation. """
        
        self.append_op_standalone(OpType.RETURN)
    
    
    def make_push_label(self, label: str) -> None:
        """ Make a push label IR operation. """
        
        self.append_op_str(OpType.PUSH_LABEL, label)
    
    
    def make_push_int(self, value: int) -> None:
        """ Make a push int IR operation. """
        
        self.append_op_int(OpType.PUSH_INT, value)
    
    
    def make_drop(self) -> None:
        """ Make a drop IR operation. """
        
        self.append_op_standalone(OpType.DROP)
    
    
    def make_print(self) -> None:
        """ Make a print IR operation. """
        
        self.append_op_standalone(OpType.PRINT)
    
    
    def append_op(self, op: Op) -> None:
        """ Append an IR operation. """
        
        self.current.ops.append(op)
    
    
    def append_op_standalone(self, type: OpType) -> None:
        """ Append a standalone IR operation. """
        
        self.append_op(Op(type))
    
    
    def append_op_int(self, type: OpType, value: int) -> None:
        """ Append an integer IR operation. """
        
        op: Op = Op(type)
        op.int_value = value
        self.append_op(op)
    
    
    def append_op_str(self, type: OpType, value: str) -> None:
        """ Append a string IR operation. """
        
        op: Op = Op(type)
        op.str_value = value
        self.append_op(op)
