from .ast.utils import print_ast
from .io.log import Log
from .parser.parser import Parser
from .parser.token import Token, TokenType

def repl() -> None:
    """ Run the Funcy REPL (Read-Evaluate-Print Loop). """
    
    print("Funcy REPL")
    print("  Enter 'exit' to exit.")
    print("  Enter 'mode (l|p)' to change mode.")
    print("  Enter 'read <path>' to read source code from <path>.\n")
    print("Parser Mode\n")
    
    mode: str = "P"
    log: Log = Log()
    parser: Parser = Parser(log)
    
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
            else:
                print(f"Failed to change to mode '{option}'!\n")
            
            continue
        elif source.startswith("read "):
            path: str = source[5:]
            
            try:
                with open(path, "rt") as file:
                    source = file.read()
            except IOError:
                print(f"Failed to read from '{path}'!\n")
                continue
        
        log.clear()
        
        if mode == "L":
            parser.lexer.begin(source)
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
            print_ast(parser.parse(source))
        
        print("")
        
        if log.has_records():
            print("--------- Error Log ---------")
            log.print_records()
            print("-----------------------------\n")
