from fy_node import Node
from fy_node_program import ProgramNode
from fy_parser import Parser
from fy_token import Token
from fy_token_type import TokenType

def main() -> None:
    """ Run a Funcy lexer and parser REPL. """
    
    def print_tree(node: Node, flags: list[bool] = []) -> None:
        """ Recursively print an AST node and its children. """
        
        for i, v in enumerate(flags):
            if i == len(flags) - 1:
                print("└───" if v else "├───", end="")
            else:
                print("    " if v else "│   ", end="")
        
        print(node)
        children: list[Node] = node.get_children()
        
        for i, v in enumerate(children):
            flags.append(i == len(children) - 1)
            print_tree(v, flags)
            flags.pop()
    
    print("Funcy Lexer and Parser REPL")
    print("Type 'exit' to exit.")
    print("Type 'read <path>' to read code from <path>.")
    print("Type 'lexer' to enter lexer mode.")
    print("Type 'parser' to enter parser mode.\n")
    print("Parser mode\n")
    parser: Parser = Parser()
    mode: str = "P"
    
    while True:
        source: str = input(f"Fy:{mode}> ")
        
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
        elif source == "lexer":
            mode = "L"
            print("Lexer mode\n")
            continue
        elif source == "parser":
            mode = "P"
            print("Parser mode\n")
            continue
        
        if mode == "L":
            parser.lexer.begin(source)
            token: Token = parser.lexer.get_token()
            print(token)
            
            while token.type != TokenType.EOF:
                token = parser.lexer.get_token()
                print(token)
            
            print("")
        elif mode == "P":
            program: ProgramNode = parser.parse(source)
            
            if parser.has_errors:
                print("")
            
            print_tree(program)
            print("")
        else:
            print(f"REPL bug: Illegal mode '{mode}'!")
            break


if __name__ == "__main__":
    main()
