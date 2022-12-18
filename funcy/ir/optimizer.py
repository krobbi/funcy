from collections.abc import Callable

from .code import Block, Code, Op, OpType

def get_code_block(code: Code, label: str) -> Block:
    """
    Get an IR block from code and a label. Return None if the block does
    not exist.
    """
    
    for block in code.blocks:
        if block.label == label:
            return block
    
    return None


def get_code_next_block(code: Code, block: Block) -> Block:
    """
    Get the IR block from code after a block. Return None if a next
    block does not exist.
    """
    
    for i in range(len(code.blocks) - 1):
        if code.blocks[i] == block:
            return code.blocks[i + 1]
    
    return None


def is_op_label(op: Op) -> bool:
    """
    Get whether an IR operation is a label. Label operations are
    operations that contain a reference to a block.
    """
    
    return op.type in (
            OpType.JUMP_LABEL, OpType.JUMP_NOT_ZERO_LABEL,
            OpType.JUMP_ZERO_LABEL, OpType.PUSH_LABEL)


def is_op_terminator(op: Op) -> bool:
    """
    Get whether an IR operation is a terminator. Terminator operations
    are operations that guarantee that any subsequent operations will
    not be executed.
    """
    
    return op.type in (OpType.HALT, OpType.JUMP_LABEL, OpType.RETURN)


def is_block_terminated(block: Block) -> bool:
    """
    Get whether an IR block is terminated. Terminated blocks are blocks
    that contain a terminator operation.
    """
    
    for op in block.ops:
        if is_op_terminator(op):
            return True
    
    return False


def optimizer_eliminate_unreachable_ops(code: Code) -> bool:
    """
    Eliminate unreachable IR operations that follow a terminator
    operation. Return whether any optimization was performed.
    """
    
    was_optimized: bool = False
    
    for block in code.blocks:
        for terminator_index in range(len(block.ops) - 1):
            if is_op_terminator(block.ops[terminator_index]):
                block.ops = block.ops[:terminator_index + 1]
                was_optimized = True
                break
    
    return was_optimized


def optimizer_eliminate_unreachable_blocks(code: Code) -> bool:
    """
    Eliminate unreachable IR blocks that are never referenced by a label
    operation or preceded by an unterminated block. Return whether any
    optimization was performed.
    """
    
    was_optimized: bool = False
    pending_blocks: list[Block] = [get_code_block(code, ".main")]
    reachable_blocks: list[Block] = []
    
    while pending_blocks:
        block: Block = pending_blocks.pop()
        
        if block is None or block in reachable_blocks:
            continue
        
        reachable_blocks.append(block)
        
        for op in block.ops:
            if is_op_label(op):
                pending_blocks.append(get_code_block(code, op.str_value))
        
        if not is_block_terminated(block):
            pending_blocks.append(get_code_next_block(code, block))
    
    for i in range(len(code.blocks) - 1, -1, -1):
        if not code.blocks[i] in reachable_blocks:
            code.blocks.pop(i)
            was_optimized = True
    
    return was_optimized


def optimize_code(code: Code) -> None:
    """ Optimize an IR code program. """
    
    OPTIMIZERS: list[Callable[[Code], bool]] = [
        optimizer_eliminate_unreachable_ops,
        optimizer_eliminate_unreachable_blocks,
    ]
    
    should_optimize: bool = True
    iterations: int = 256
    
    while should_optimize and iterations > 0:
        should_optimize = False
        iterations -= 1
        
        for optimizer in OPTIMIZERS:
            if optimizer(code):
                should_optimize = True
