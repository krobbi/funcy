from .nodes import *

def get_node_children(node: Node) -> list[Node]:
    """ Get a node's children as a list. """
    
    if isinstance(node, RootNode):
        return node.stmts
    elif isinstance(node, FuncStmtNode):
        result: list[Node] = [node.name]
        result.extend(node.params)
        result.append(node.stmt)
        return result
    elif isinstance(node, BlockStmtNode):
        return node.stmts
    elif isinstance(node, IfStmtNode):
        return [node.expr, node.stmt]
    elif isinstance(node, ReturnExprStmtNode):
        return [node.expr]
    elif isinstance(node, PrintStmtNode):
        return [node.expr]
    elif isinstance(node, ExprStmtNode):
        return [node.expr]
    elif isinstance(node, CallExprNode):
        result: list[ExprNode] = [node.callee]
        result.extend(node.params)
        return result
    elif isinstance(node, UnExprNode):
        return [node.expr]
    elif isinstance(node, BinExprNode):
        return [node.lhs, node.rhs]
    
    return []


def print_ast(node: Node, flags: list[bool] = []) -> None:
    """ Recursively print an AST node and its children as a tree. """
    
    for i, v in enumerate(flags):
        if i == len(flags) - 1:
            print("└───" if v else "├───", end="")
        else:
            print("    " if v else "│   ", end="")
    
    print(node)
    
    children: list[Node] = get_node_children(node)
    
    for i, v in enumerate(children):
        flags.append(i == len(children) - 1)
        print_ast(v, flags)
        flags.pop()
