from fy_ir_block import IRBlock
from fy_ir_op import IROp
from fy_ir_op_type import IROpType

class IRCode:
    """ An IR program. """
    
    label_count: int = 0
    """ The IR code's label count. """
    
    current: IRBlock
    """ The IR code's current IR block. """
    
    blocks: list[IRBlock]
    """ The IR codes's IR blocks. """
    
    def __init__(self) -> None:
        """ Initialize the IR code's current IR block and IR blocks. """
        
        self.current = IRBlock(".main")
        self.blocks = [self.current]
    
    
    def get_label(self) -> str:
        """ Get the current label. """
        
        return self.current.label
    
    
    def set_label(self, label: str) -> None:
        """ Set the current label. """
        
        for block in self.blocks:
            if block.label == label:
                self.current = block
                return
    
    
    def insert_label(self, name: str) -> str:
        """ Insert a label after the current label. """
        
        self.label_count += 1
        label: str = f".L{self.label_count}_{name}"
        index: int = len(self.blocks)
        
        for i in range(index):
            if self.blocks[i] == self.current:
                index = i + 1
                break
        
        self.blocks.insert(index, IRBlock(label))
        return label
    
    
    def make_halt(self) -> None:
        """ Make a halt IR operation in the current label. """
        
        self.current.ops.append(IROp(IROpType.HALT))
    
    
    def make_no_operation(self) -> None:
        """ Make a no operation IR operation in the current label. """
        
        self.current.ops.append(IROp(IROpType.NO_OPERATION))
    
    
    def make_branch_always_label(self, label: str) -> None:
        """ Make a branch always label IR operation in the current label. """
        
        op: IROp = IROp(IROpType.BRANCH_ALWAYS_LABEL)
        op.str_value = label
        self.current.ops.append(op)
    
    
    def make_call_argc(self, argc: int) -> None:
        """ Make a call argc IR operation in the current label. """
        
        op: IROp = IROp(IROpType.CALL_ARGC)
        op.int_value = argc
        self.current.ops.append(op)
    
    
    def make_return(self) -> None:
        """ Make a return IR operation in the current label. """
        
        self.current.ops.append(IROp(IROpType.RETURN))
    
    
    def make_push_label(self, label: str) -> None:
        """ Make a push label IR operation in the current label. """
        
        op: IROp = IROp(IROpType.PUSH_LABEL)
        op.str_value = label
        self.current.ops.append(op)
    
    
    def make_push_int(self, value: int) -> None:
        """ Make a push int IR operation in the current label. """
        
        op: IROp = IROp(IROpType.PUSH_INT)
        op.int_value = value
        self.current.ops.append(op)
    
    
    def make_discard(self) -> None:
        """ Make a discard IR operation in the current label. """
        
        self.current.ops.append(IROp(IROpType.DISCARD))
    
    
    def make_print(self) -> None:
        """ Make a print IR operation in the current label. """
        
        self.current.ops.append(IROp(IROpType.PRINT))
