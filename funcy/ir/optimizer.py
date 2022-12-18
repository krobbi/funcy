from collections.abc import Callable

from .code import Code, Op, OpType

def is_op_terminator(op: Op) -> bool:
    """
    Get whether an IR operation is a terminator. Terminator operations
    are operations that guarantee that any subsequent operations will
    not be executed.
    """
    return op.type in (OpType.HALT, OpType.JUMP_LABEL, OpType.RETURN)


def optimizer_eliminate_unreachable_ops(code: Code) -> bool:
    """
    Eliminates unreachable IR operations that follow a terminator
    operation. Returns whether any optimization was performed.
    """
    
    was_optimized: bool = False
    
    for block in code.blocks:
        for terminator_index in range(len(block.ops) - 1):
            if is_op_terminator(block.ops[terminator_index]):
                block.ops = block.ops[:terminator_index + 1]
                was_optimized = True
                break
    
    return was_optimized


def optimize_code(code: Code) -> None:
    """ Optimize an IR code program. """
    
    OPTIMIZERS: list[Callable[[Code], bool]] = [
        optimizer_eliminate_unreachable_ops,
    ]
    
    should_optimize: bool = True
    iterations: int = 256
    
    while should_optimize and iterations > 0:
        should_optimize = False
        iterations -= 1
        
        for optimizer in OPTIMIZERS:
            if optimizer(code):
                should_optimize = True
