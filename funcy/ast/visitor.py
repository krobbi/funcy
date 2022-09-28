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
        elif isinstance(node, IfStmtNode):
            self.visit_if_stmt(node, code)
        elif isinstance(node, IfElseStmtNode):
            self.visit_if_else_stmt(node, code)
        elif isinstance(node, NopStmtNode):
            self.visit_nop_stmt(node, code)
        elif isinstance(node, ReturnStmtNode):
            self.visit_return_stmt(node, code)
        elif isinstance(node, ReturnExprStmtNode):
            self.visit_return_expr_stmt(node, code)
        elif isinstance(node, PrintStmtNode):
            self.visit_print_stmt(node, code)
        elif isinstance(node, ExprStmtNode):
            self.visit_expr_stmt(node, code)
        elif isinstance(node, IntExprNode):
            self.visit_int_expr(node, code)
        elif isinstance(node, IdentifierExprNode):
            self.visit_identifier_expr(node, code)
        elif isinstance(node, CallExprNode):
            self.visit_call_expr(node, code)
        elif isinstance(node, AndExprNode):
            self.visit_and_expr(node, code)
        elif isinstance(node, OrExprNode):
            self.visit_or_expr(node, code)
        elif isinstance(node, UnExprNode):
            self.visit_un_expr(node, code)
        elif isinstance(node, BinExprNode):
            self.visit_bin_expr(node, code)
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
    
    
    def visit_if_stmt(self, node: IfStmtNode, code: Code) -> None:
        """ Visit an if statement node. """
        
        end_label: str = code.insert_label("if_end")
        self.visit(node.expr, code)
        code.make_jump_zero_label(end_label)
        
        self.scope_stack.push()
        self.visit(node.stmt, code)
        self.scope_stack.pop()
        
        code.set_label(end_label)
    
    
    def visit_if_else_stmt(self, node: IfElseStmtNode, code: Code) -> None:
        """ Visit an if else statement node. """
        
        end_label: str = code.insert_label("if_else_end")
        else_label: str = code.insert_label("if_else_else")
        self.visit(node.expr, code)
        code.make_jump_zero_label(else_label)
        
        self.scope_stack.push()
        self.visit(node.then_stmt, code)
        code.make_jump_label(end_label)
        self.scope_stack.pop()
        
        code.set_label(else_label)
        self.scope_stack.push()
        self.visit(node.else_stmt, code)
        self.scope_stack.pop()
        
        code.set_label(end_label)
    
    
    def visit_nop_stmt(self, node: NopStmtNode, code: Code) -> None:
        """ Visit a no operation statement node. """
        
        pass # No operation statements should have no effect.
    
    
    def visit_return_stmt(self, node: ReturnStmtNode, code: Code) -> None:
        """ Visit a return statement node. """
        
        code.make_push_int(0)
        code.make_return()
    
    
    def visit_return_expr_stmt(
            self, node: ReturnExprStmtNode, code: Code) -> None:
        """ Visit a return expression statement node. """
        
        self.visit(node.expr, code)
        code.make_return()
    
    
    def visit_print_stmt(self, node: PrintStmtNode, code: Code) -> None:
        """ Visit a print statement node. """
        
        self.visit(node.expr, code)
        code.make_print()
    
    
    def visit_expr_stmt(self, node: ExprStmtNode, code: Code) -> None:
        """ Visit an expression statement node. """
        
        self.visit(node.expr, code)
        code.make_drop()
    
    
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
            code.make_load_local_offset(symbol.int_value)
        else:
            self.log_error(
                    "Bug: Unimplemented symbol access "
                    f"'{symbol.access.name}' at '{node.name}'!", node)
            code.make_push_int(0)
    
    
    def visit_call_expr(self, node: CallExprNode, code: Code) -> None:
        """ Visit a call expression node. """
        
        is_callable: bool = False
        
        # Number of parameters expected. -1 for any number.
        expected_params: int = -1
        
        if isinstance(node.callee, IntExprNode):
            self.log_error(
                    f"Called the integer value '{node.callee.value}' "
                    "as a function!", node.callee)
        elif isinstance(node.callee, IdentifierExprNode):
            symbol: Symbol = self.scope_stack.get(node.callee.name)
            
            if symbol.access == SymbolAccess.UNDEFINED:
                self.log_error(
                        f"Called function name '{symbol.name}' is undefined "
                        "in the current scope!", node.callee)
            elif symbol.access == SymbolAccess.FUNC:
                is_callable = True
                expected_params = symbol.int_value
            elif symbol.access == SymbolAccess.LOCAL:
                is_callable = True # A local may contain a function.
            else:
                self.log_error(
                        "Bug: Unimplemented callee symbol access "
                        f"'{symbol.access.name}' at '{node.callee}'!",
                        node.callee)
        elif isinstance(node.callee, CallExprNode):
            is_callable = True # A call may return a function.
        else:
            self.log_error(
                    "Bug: Unimplemented callee expression type "
                    f"for '{node.callee}'!", node.callee)
        
        for param in node.params:
            self.visit(param, code)
        
        # Drop our parameters if we can't make the call.
        if not is_callable:
            for i in range(len(node.params)):
                code.make_drop()
            
            code.make_push_int(0)
            return
        
        if expected_params == -1:
            expected_params = len(node.params)
        elif len(node.params) != expected_params:
            if expected_params == 1:
                self.log_error(
                        "Called function expected 1 parameter, "
                        f"got {len(node.params)}!", node)
            else:
                self.log_error(
                        f"Called function expected {expected_params} "
                        f"parameters, got {len(node.params)}!", node)
            
            difference: int = len(node.params) - expected_params
            
            # Insert missing parameters.
            while difference < 0:
                code.make_push_int(0)
                difference += 1
            
            # Or drop excess parameters.
            while difference > 0:
                code.make_drop()
                difference -= 1
        
        self.visit(node.callee, code)
        code.make_call_paramc(expected_params)
    
    
    def visit_and_expr(self, node: AndExprNode, code: Code) -> None:
        """ Visit an and expression node. """
        
        short_label: str = code.insert_label("and_short")
        self.visit(node.lhs_expr, code)
        code.make_duplicate()
        code.make_jump_zero_label(short_label)
        
        code.make_drop()
        self.visit(node.rhs_expr, code)
        
        code.set_label(short_label)
    
    
    def visit_or_expr(self, node: OrExprNode, code: Code) -> None:
        """ Visit an or expression node. """
        
        short_label: str = code.insert_label("or_short")
        self.visit(node.lhs_expr, code)
        code.make_duplicate()
        code.make_jump_not_zero_label(short_label)
        
        code.make_drop()
        self.visit(node.rhs_expr, code)
        
        code.set_label(short_label)
    
    
    def visit_un_expr(self, node: UnExprNode, code: Code) -> None:
        """ Visit a unary expression node. """
        
        self.visit(node.expr, code)
        
        if node.op == UnOp.AFFIRM:
            pass # A prefixed '+' operator should have no effect.
        elif node.op == UnOp.NEGATE:
            code.make_unary_negate()
        elif node.op == UnOp.NOT:
            code.make_unary_not()
        else:
            self.log_error(
                    f"Bug: Unimplemented unary operator '{node.op.name}'!",
                    node)
    
    
    def visit_bin_expr(self, node: BinExprNode, code: Code) -> None:
        """ Visit a binary expression node. """
        
        self.visit(node.lhs_expr, code)
        self.visit(node.rhs_expr, code)
        
        if node.op == BinOp.ADD:
            code.make_binary_add()
        elif node.op == BinOp.SUBTRACT:
            code.make_binary_subtract()
        elif node.op == BinOp.MULTIPLY:
            code.make_binary_multiply()
        elif node.op == BinOp.DIVIDE:
            code.make_binary_divide()
        elif node.op == BinOp.MODULO:
            code.make_binary_modulo()
        elif node.op == BinOp.EQUALS:
            code.make_binary_equals()
        elif node.op == BinOp.NOT_EQUALS:
            code.make_binary_not_equals()
        elif node.op == BinOp.GREATER:
            code.make_binary_greater()
        elif node.op == BinOp.GREATER_EQUALS:
            code.make_binary_greater_equals()
        elif node.op == BinOp.LESS:
            code.make_binary_less()
        elif node.op == BinOp.LESS_EQUALS:
            code.make_binary_less_equals()
        elif node.op == BinOp.AND:
            code.make_binary_and()
        elif node.op == BinOp.OR:
            code.make_binary_or()
        else:
            self.log_error(
                    f"Bug: Unimplemented binary operator '{node.op.name}'!",
                    node)
            code.make_drop() # Preserve stack size.
