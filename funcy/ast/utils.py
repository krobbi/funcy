from .nodes import Node

def print_ast(node: Node, flags: list[bool] = []) -> None:
    """ Recursively print an AST node and its children as a tree. """
    
    for i, v in enumerate(flags):
        if i == len(flags) - 1:
            print("└───" if v else "├───", end="")
        else:
            print("    " if v else "│   ", end="")
    
    print(node)
    children: list[Node] = node.get_children()
    
    for i, v in enumerate(children):
        flags.append(i == len(children) - 1)
        print_ast(v, flags)
        flags.pop()


del Node
