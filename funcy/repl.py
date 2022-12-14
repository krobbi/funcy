from .ast.utils import print_ast
from .ast.visitor import Visitor
from .fvm import FVM
from .io.input_wrapper import InputWrapper
from .io.log import Log
from .ir.serializer import Serializer
from .ir.utils import print_code
from .parser.parser import Parser
from .parser.token import Token, TokenType

def repl() -> None:
    """ Run the Funcy REPL (Read-Evaluate-Print Loop). """
    
    print("Funcy REPL")
    print("  Enter 'exit' to exit.")
    print("  Enter 'mode (l|p|g|i)' to change mode.")
    print("  Enter 'read <path>' to read source code from <path>.\n")
    print("Interpreter Mode\n")
    
    mode: str = "I"
    input_wrapper: InputWrapper = InputWrapper()
    log: Log = Log()
    parser: Parser = Parser(log)
    visitor: Visitor = Visitor(log)
    serializer: Serializer = Serializer()
    fvm: FVM = FVM()
    
    while True:
        source: str = input(f"Funcy:{mode}> ")
        
        if source == "exit":
            break
        elif source.startswith("mode "):
            option: str = source[5:]
            
            if option == "l":
                mode = "L"
                print("Lexer Mode\n")
            elif option == "p":
                mode = "P"
                print("Parser Mode\n")
            elif option == "g":
                mode = "G"
                print("Generator Mode\n")
            elif option == "i":
                mode = "I"
                print("Interpreter Mode\n")
            else:
                print(f"Failed to change to mode '{option}'!\n")
            
            continue
        elif source.startswith("read "):
            input_wrapper.from_path(source[5:])
        else:
            input_wrapper.from_source(source)
        
        if not input_wrapper.is_ok:
            print(f"Failed to read from '{input_wrapper.path}'!\n")
            continue
        
        log.clear()
        
        if mode == "L":
            if input_wrapper.is_binary:
                print("Lexer mode expects source code!\n")
                continue
            
            parser.lexer.begin(input_wrapper.source)
            token: Token = parser.lexer.get_token()
            tokens: list[Token] = []
            
            if token.type == TokenType.ERROR:
                log.log(token.str_value, token.span)
            else:
                tokens.append(token)
            
            while token.type != TokenType.EOF:
                token = parser.lexer.get_token()
                
                if token.type == TokenType.ERROR:
                    log.log(token.str_value, token.span)
                else:
                    tokens.append(token)
            
            for token in tokens:
                print(token)
        elif mode == "P":
            if input_wrapper.is_binary:
                print("Parser mode expects source code!\n")
                continue
            
            print_ast(parser.parse(input_wrapper.source))
        elif mode == "G":
            if input_wrapper.is_binary:
                print("Generator mode expects source code!\n")
                continue
            
            print_code(visitor.generate(parser.parse(input_wrapper.source)))
        elif mode == "I":
            if not input_wrapper.is_binary:
                input_wrapper.bytecode = serializer.serialize(visitor.generate(
                        parser.parse(input_wrapper.source)), False)
            
            if log.has_records():
                print("Refused to run FVM! Fix errors first:")
            else:
                if not fvm.load(input_wrapper.bytecode):
                    print("Failed to load FVM bytecode!\n")
                    continue
                
                if not fvm.begin():
                    print("Failed to start FVM!\n")
                    continue
                
                while fvm.ef:
                    fvm.step()
                
                print(f"FVM finished with exit code '{fvm.ec}'!")
        
        print("")
        
        if log.has_records():
            print("--------- Error Log ---------")
            log.print_records()
            print("-----------------------------\n")
