from .ast.visitor import Visitor
from .fvm import FVM
from .io.input_wrapper import InputWrapper
from .io.log import Log
from .ir.code import Code
from .ir.serializer import Serializer
from .parser.parser import Parser

def get_error_bytecode() -> bytes:
    """ Builds error FVM bytecode. """
    
    code: Code = Code()
    code.make_push_int(1)
    code.make_halt()
    return Serializer().serialize(code, False)


def build(in_path: str, out_path: str) -> None:
    """
    Build Funcy source code from an input path to FVM bytecode at an
    output path.
    """
    
    bytecode: bytes = compile_path(in_path)
    
    try:
        with open(out_path, "wb") as file:
            file.write(bytecode)
    except IOError:
        print(f"Failed to build to '{out_path}'!")


def compile(source: str) -> bytes:
    """ Compile Funcy source code to FVM bytecode. """
    
    log: Log = Log()
    code: Code = Visitor(log).generate(Parser(log).parse(source))
    
    if log.has_records():
        log.print_records()
        return get_error_bytecode()
    
    return Serializer().serialize(code, False)


def compile_path(path: str) -> bytes:
    """ Compile Funcy source code to FVM bytecode from a path. """
    
    input_wrapper: InputWrapper = InputWrapper()
    input_wrapper.from_path(path)
    
    if not input_wrapper.is_ok:
        print(f"Failed to build from '{path}'!")
        return get_error_bytecode()
    
    if input_wrapper.is_binary:
        return input_wrapper.bytecode
    
    return compile(input_wrapper.source)


def exec(source: str | bytes) -> int:
    """
    Execute Funcy source code or FVM bytecode and return an exit code.
    """
    
    if isinstance(source, str):
        source = compile(source)
    elif not isinstance(source, bytes):
        return 1
    
    fvm: FVM = FVM()
    
    if not fvm.load(source):
        print("Failed to load bytecode!")
        return 1
    
    if not fvm.begin():
        print("Failed to start FVM!")
        return 1
    
    while fvm.ef:
        fvm.step()
    
    return fvm.ec


def exec_path(path: str) -> int:
    """
    Execute Funcy source code or FVM bytecode from a path and return an
    exit code.
    """
    
    input_wrapper: InputWrapper = InputWrapper()
    input_wrapper.from_path(path)
    
    if not input_wrapper.is_ok:
        print(f"Failed to execute from '{path}'!")
        return 1
    
    if input_wrapper.is_binary:
        return exec(input_wrapper.bytecode)
    else:
        return exec(input_wrapper.source)
