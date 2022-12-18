from collections.abc import Callable

from .code import Code

def optimize_code(code: Code) -> None:
    """ Optimize an IR code program. """
    
    OPTIMIZERS: list[Callable[[Code], bool]] = []
    
    should_optimize: bool = True
    iterations: int = 256
    
    while should_optimize and iterations > 0:
        should_optimize = False
        iterations -= 1
        
        for optimizer in OPTIMIZERS:
            if optimizer(code):
                should_optimize = True
