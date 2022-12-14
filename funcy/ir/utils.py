from .ircode import Code

def print_code(code: Code) -> None:
    """ Print an IR code program. """
    
    for block in code.blocks:
        print(block)
        
        for op in block.ops:
            print(f"    {op}")
