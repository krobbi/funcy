from enum import Enum, auto

class OpType(Enum):
    """ The type of an IR operation. """
    
    HALT = auto()
    """ Pop and halt element. """
    
    JUMP_ZERO_LABEL = auto()
    """ Pop and jump if zero with label. """
    
    CALL_PARAMC = auto()
    """ Call with parameter count. """
    
    RETURN = auto()
    """ Pop and return element. """
    
    DROP = auto()
    """ Pop and discard element. """
    
    PUSH_LABEL = auto()
    """ Push labeled address. """
    
    PUSH_INT = auto()
    """ Push integer value. """
    
    LOAD_LOCAL_OFFSET = auto()
    """ Load local with offset. """
    
    STORE_LOCAL_OFFSET = auto()
    """ Store local with offset. """
    
    UNARY_NEGATE = auto()
    """ Pop, negate, and push element. """
    
    BINARY_ADD = auto()
    """ Pop, add, and push elements. """
    
    BINARY_SUBTRACT = auto()
    """ Pop, subtract, and push elements. """
    
    BINARY_MULTIPLY = auto()
    """ Pop, multiply, and push elements. """
    
    BINARY_DIVIDE = auto()
    """ Pop, divide, and push elements. """
    
    BINARY_MODULO = auto()
    """ Pop, modulo, and push elements. """
    
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
        
        if self.type in (
                OpType.CALL_PARAMC, OpType.PUSH_INT,
                OpType.LOAD_LOCAL_OFFSET, OpType.STORE_LOCAL_OFFSET):
            return f"{self.type.name} {self.int_value};"
        elif self.type in (OpType.JUMP_ZERO_LABEL, OpType.PUSH_LABEL):
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
    
    
    def insert_label(self, name: str) -> str:
        """ Insert a label after the current label. """
        
        index: int = len(self.blocks)
        
        for i in range(index):
            if self.current == self.blocks[i]:
                index = i + 1
                break
        
        self.label_count += 1
        label: str = f".L{self.label_count}_{name}"
        self.blocks.insert(index, Block(label))
        return label
    
    
    def make_halt(self) -> None:
        """ Make a halt IR operation. """
        
        self.append_op_standalone(OpType.HALT)
    
    
    def make_jump_zero_label(self, label: str) -> None:
        """ Make a jump zero label IR operation. """
        
        self.append_op_str(OpType.JUMP_ZERO_LABEL, label)
    
    
    def make_call_paramc(self, paramc: int) -> None:
        """ Make a call paramc IR operation. """
        
        self.append_op_int(OpType.CALL_PARAMC, paramc)
    
    
    def make_return(self) -> None:
        """ Make a return IR operation. """
        
        self.append_op_standalone(OpType.RETURN)
    
    
    def make_drop(self) -> None:
        """ Make a drop IR operation. """
        
        self.append_op_standalone(OpType.DROP)
    
    
    def make_push_label(self, label: str) -> None:
        """ Make a push label IR operation. """
        
        self.append_op_str(OpType.PUSH_LABEL, label)
    
    
    def make_push_int(self, value: int) -> None:
        """ Make a push int IR operation. """
        
        self.append_op_int(OpType.PUSH_INT, value)
    
    
    def make_load_local_offset(self, offset: int) -> None:
        """ Make a load local offset IR operation. """
        
        self.append_op_int(OpType.LOAD_LOCAL_OFFSET, offset)
    
    
    def make_store_local_offset(self, offset: int) -> None:
        """ Make a store local offset IR operation. """
        
        self.append_op_int(OpType.STORE_LOCAL_OFFSET, offset)
    
    
    def make_unary_negate(self) -> None:
        """ Make a unary negate IR operation. """
        
        self.append_op_standalone(OpType.UNARY_NEGATE)
    
    
    def make_binary_add(self) -> None:
        """ Make a binary add IR operation. """
        
        self.append_op_standalone(OpType.BINARY_ADD)
    
    
    def make_binary_subtract(self) -> None:
        """ Make a binary subtract IR operation. """
        
        self.append_op_standalone(OpType.BINARY_SUBTRACT)
    
    
    def make_binary_multiply(self) -> None:
        """ Make a binary multiply IR operation. """
        
        self.append_op_standalone(OpType.BINARY_MULTIPLY)
    
    
    def make_binary_divide(self) -> None:
        """ Make a binary divide IR operation. """
        
        self.append_op_standalone(OpType.BINARY_DIVIDE)
    
    
    def make_binary_modulo(self) -> None:
        """ Make a binary modulo IR operation. """
        
        self.append_op_standalone(OpType.BINARY_MODULO)
    
    
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
