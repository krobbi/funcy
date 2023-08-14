from collections.abc import Callable

from .code import Code

class Intrinsic:
    """ An intrinsic function. """
    
    arity: int
    """ The intrinsic function's arity. """
    
    generator: Callable[[Code], None]
    """ The intrinsic function's generator. """
    
    def __init__(self, arity: int, generator: Callable[[Code], None]) -> None:
        """ Initialize the intrinsic function's arity and generator. """
        
        self.arity = arity
        self.generator = generator


def generate_chr_at(code: Code) -> None:
    """ Generate a chrAt intrinsic. """
    
    code.make_binary_add()
    code.make_unary_dereference()


def generate_put_chr(code: Code) -> None:
    """ Generate a putChr intrinsic. """
    
    code.make_put_chr()


def get_intrinsics() -> dict[str, Intrinsic]:
    """ Get a dictionary of intrinsics. """
    
    return {
        "chrAt": Intrinsic(2, generate_chr_at),
        "putChr": Intrinsic(1, generate_put_chr),
    }
