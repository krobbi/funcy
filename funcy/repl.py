from .parser.lexer import Lexer
from .parser.token import Token, TokenType

def repl() -> None:
    """ Run the Funcy REPL (Read-Evaluate-Print Loop). """
    
    print("Funcy REPL")
    print("  Enter 'exit' to exit.")
    print("  Enter 'read <path>' to read source code from <path>.\n")
    print("Lexer Mode\n")
    
    lexer: Lexer = Lexer()
    
    while True:
        source: str = input("Funcy:L> ")
        
        if source == "exit":
            break
        elif source.startswith("read "):
            path: str = source[5:]
            
            try:
                with open(path, "rt") as file:
                    source = file.read()
            except IOError:
                print(f"Failed to read from '{path}'!\n")
                continue
        
        lexer.begin(source)
        token: Token = lexer.get_token()
        print(token)
        
        while token.type != TokenType.EOF:
            token = lexer.get_token()
            print(token)
        
        print("")
