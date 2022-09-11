from fy_lexer import Lexer
from fy_token import Token
from fy_token_type import TokenType

def main() -> None:
    """ Run a Funcy lexer REPL. """
    
    print("Funcy Lexer REPL")
    print("Type 'exit' to exit.")
    print("Type 'read <path>' to read code from <path>.\n")
    lexer: Lexer = Lexer()
    
    while True:
        source: str = input("FyLR> ")
        
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


if __name__ == "__main__":
    main()
