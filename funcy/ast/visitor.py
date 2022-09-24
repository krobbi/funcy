from ..io.log import Log
from ..ir.code import Code
from ..parser.position import Span
from .nodes import *
from .scope import ScopeStack, Symbol, SymbolAccess

class Visitor:
    """
    Visits an abstract syntax tree's nodes to perform semantic
    validation and code generation.
    """
    
    log: Log
    """ The visitor's log. """
    
    scope_stack: ScopeStack
    """ The visitor's scope stack. """
    
    def __init__(self, log: Log) -> None:
        """ Initialize the visitor's log and scope stack. """
        
        self.log = log
        self.scope_stack = ScopeStack(log)
    
    
    def generate(self, ast: RootNode) -> Code:
        """ Generate IR code from an abstract syntax tree. """
        
        self.scope_stack.clear()
        
        code: Code = Code()
        self.visit(ast, code)
        
        return code
    
    
    def log_error(self, message: str, span: Span | Node = None) -> None:
        """ Log an error message at a span. """
        
        if isinstance(span, Span):
            span = span.copy()
        elif isinstance(span, Node):
            span = span.span.copy()
        elif not span is None:
            self.log.log(f"Bug: Logged an error with a non-span '{span}'!")
            span = None
        
        self.log.log(message, span)
    
    
    def visit(self, node: Node, code: Code) -> None:
        """ Visit an abstract syntax tree node. """
        
        if isinstance(node, RootNode):
            self.visit_root(node, code)
        elif isinstance(node, FuncStmtNode):
            self.visit_func_stmt(node, code)
        elif isinstance(node, BlockStmtNode):
            self.visit_block_stmt(node, code)
        elif isinstance(node, NopStmtNode):
            self.visit_nop_stmt(node, code)
        elif isinstance(node, PrintStmtNode):
            self.visit_print_stmt(node, code)
        elif isinstance(node, ExprStmtNode):
            self.visit_expr_stmt(node, code)
        elif isinstance(node, IntExprNode):
            self.visit_int_expr(node, code)
        elif isinstance(node, IdentifierExprNode):
            self.visit_identifier_expr(node, code)
        else:
            self.log_error(f"Unimplemented visitor for '{node}'!", node)
    
    
    def visit_root(self, node: RootNode, code: Code) -> None:
        """ Visit a root node. """
        
        self.scope_stack.push()
        main_label: str = code.get_label()
        
        for stmt in node.stmts:
            self.visit(stmt, code)
        
        code.set_label(main_label)
        main_symbol: Symbol = self.scope_stack.get("main")
        
        if main_symbol.access == SymbolAccess.FUNC:
            for i in range(main_symbol.int_value):
                code.make_push_int(0)
            
            code.make_push_label(main_symbol.str_value)
            code.make_call_paramc(main_symbol.int_value)
        else:
            code.make_push_int(0)
        
        code.make_halt()
        self.scope_stack.pop()
    
    
    def visit_func_stmt(self, node: FuncStmtNode, code: Code) -> None:
        """ Visit a function statement node. """
        
        name: str = node.name.name
        parent_label: str = code.get_label()
        func_label: str = code.append_label(f"func_{name}")
        code.set_label(func_label)
        
        if self.scope_stack.has(name):
            self.log_error(
                    f"Funcion name '{name}' is already defined "
                    "in the current scope!", node.name)
        else:
            self.scope_stack.define_func(name, func_label, len(node.params))
        
        self.scope_stack.push()
        self.scope_stack.undefine_locals()
        self.scope_stack.push()
        
        for param in node.params:
            if self.scope_stack.has(param.name):
                self.log_error(
                        f"Parameter name '{param.name}' is already defined "
                        f"in {name}'s parameter list!", param)
                continue
            
            self.scope_stack.define_local(param.name)
        
        self.scope_stack.push()
        self.visit(node.stmt, code)
        code.make_push_int(0)
        code.make_return()
        self.scope_stack.pop()
        self.scope_stack.pop()
        self.scope_stack.pop()
        code.set_label(parent_label)
    
    
    def visit_block_stmt(self, node: BlockStmtNode, code: Code) -> None:
        """ Visit a block statement node. """
        
        self.scope_stack.push()
        
        for stmt in node.stmts:
            self.visit(stmt, code)
        
        self.scope_stack.pop()
    
    
    def visit_nop_stmt(self, node: NopStmtNode, code: Code) -> None:
        """ Visit a no operation statement node. """
        
        pass # No operation statements should have no effect.
    
    
    def visit_print_stmt(self, node: PrintStmtNode, code: Code) -> None:
        """ Visit a print statement node. """
        
        self.visit(node.expr, code)
        code.make_print()
    
    
    def visit_expr_stmt(self, node: ExprStmtNode, code: Code) -> None:
        """ Visit an expression statement node. """
        
        self.visit(node.expr, code)
        code.make_discard()
    
    
    def visit_int_expr(self, node: IntExprNode, code: Code) -> None:
        """ Visit an integer expression node. """
        
        code.make_push_int(node.value)
    
    
    def visit_identifier_expr(
            self, node: IdentifierExprNode, code: Code) -> None:
        """ Visit an identifier expression node. """
        
        symbol: Symbol = self.scope_stack.get(node.name)
        
        if symbol.access == SymbolAccess.UNDEFINED:
            self.log_error(
                    f"Identifier '{node.name}' is undefined "
                    "in the current scope!", node)
            code.make_push_int(0)
        elif symbol.access == SymbolAccess.FUNC:
            code.make_push_label(symbol.str_value)
        elif symbol.access == SymbolAccess.LOCAL:
            self.log_error("Function parameters are unimplemented!", node)
            code.make_push_int(0)
        else:
            self.log_error(
                    "Bug: Unimplemented symbol access "
                    f"'{symbol.access.name}' at '{node.name}'!", node)
            code.make_push_int(0)
