from fvm import FVM
from fy_ir_code import IRCode
from fy_ir_generator import IRGenerator
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
    
    
    def print_ir(code: IRCode) -> None:
        """ Print IR code. """
        
        for block in code.blocks:
            print(block)
            
            for op in block.ops:
                print(f"    {op}")
    
    
    print("Funcy Lexer and Parser REPL")
    print("Type 'exit' to exit.")
    print("Type 'read <path>' to read code from <path>.")
    print("Type 'lexer' to enter lexer mode.")
    print("Type 'parser' to enter parser mode.")
    print("Type 'interpreter' to enter interpreter mode.\n")
    print("Interpreter mode\n")
    parser: Parser = Parser()
    generator: IRGenerator = IRGenerator()
    fvm: FVM = FVM()
    mode: str = "I"
    
    while True:
        is_bytecode: bool = False
        source: str = input(f"Fy:{mode}> ")
        bytecode: bytes = bytes()
        
        if source == "exit":
            break
        elif source.startswith("read "):
            path: str = source[5:]
            
            try:
                with open(path, "rb") as file:
                    bytecode = file.read()
                
                if len(bytecode) >= 16 and bytecode[0:8] == fvm.HEADER:
                    is_bytecode = True
                else:
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
        elif source == "interpreter":
            mode = "I"
            print("Interpreter mode\n")
            continue
        
        if mode == "L":
            if is_bytecode:
                print("Lexer mode expects Funcy source code!\n")
                continue
            
            parser.lexer.begin(source)
            token: Token = parser.lexer.get_token()
            print(token)
            
            while token.type != TokenType.EOF:
                token = parser.lexer.get_token()
                print(token)
            
            print("")
        elif mode == "P":
            if is_bytecode:
                print("Parser mode expects Funcy source code!\n")
                continue
            
            ast: ProgramNode = parser.parse(source)
            
            if parser.has_errors:
                print("")
            
            print_tree(ast)
            print("")
        elif mode == "I":
            if is_bytecode:
                if not fvm.load(bytecode):
                    print("Failed to load FVM bytecode!\n")
                    continue
                elif not fvm.begin():
                    print("Failed to start FVM!\n")
                    continue
                
                while fvm.ef:
                    fvm.step()
                
                print(f"\nFVM finished with exit code {fvm.ec}.\n")
            else:
                ast: ProgramNode = parser.parse(source)
                code: IRCode = generator.generate(ast)
                
                if parser.has_errors or generator.has_errors:
                    print("")
                
                print_ir(code)
                print("")
        else:
            print(f"REPL bug: Illegal mode '{mode}'!")
            break


if __name__ == "__main__":
    main()
