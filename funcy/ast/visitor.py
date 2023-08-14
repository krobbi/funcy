from ..io.log import Log
from ..ir.code import Code
from ..ir.intrinsics import Intrinsic, get_intrinsics
from ..ir.optimizer import optimize_code
from ..parser.position import Span
from .nodes import *
from .scope import ScopeStack, ScopedLabel, Symbol, SymbolAccess

class Visitor:
    """
    Visits an abstract syntax tree's nodes to perform semantic
    validation and code generation.
    """
    
    log: Log
    """ The visitor's log. """
    
    intrinsics: dict[str, Intrinsic]
    """ The visitor's intrinsics. """
    
    scope_stack: ScopeStack
    """ The visitor's scope stack. """
    
    def __init__(self, log: Log) -> None:
        """ Initialize the visitor's log and scope stack. """
        
        self.log = log
        self.intrinsics = get_intrinsics()
        self.scope_stack = ScopeStack(log)
    
    
    def generate(self, ast: RootNode) -> Code:
        """ Generate IR code from an abstract syntax tree. """
        
        self.scope_stack.clear()
        
        code: Code = Code()
        self.visit(ast, code)
        optimize_code(code)
        
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
    
    
    def pop_scope(self, code: Code) -> None:
        """ Pop the current scope and discard its locals. """
        
        for i in range(self.scope_stack.get_scope_local_count()):
            code.make_drop()
        
        self.scope_stack.pop()
    
    
    def visit(self, node: Node, code: Code) -> None:
        """ Visit an abstract syntax tree node. """
        
        if isinstance(node, RootNode):
            self.visit_root(node, code)
        elif isinstance(node, ModuleNode):
            self.visit_module(node, code)
        elif isinstance(node, IntrinsicStmtNode):
            self.visit_intrinsic_stmt(node, code)
        elif isinstance(node, FuncStmtNode):
            self.visit_func_stmt(node, code)
        elif isinstance(node, BlockStmtNode):
            self.visit_block_stmt(node, code)
        elif isinstance(node, IfStmtNode):
            self.visit_if_stmt(node, code)
        elif isinstance(node, IfElseStmtNode):
            self.visit_if_else_stmt(node, code)
        elif isinstance(node, WhileStmtNode):
            self.visit_while_stmt(node, code)
        elif isinstance(node, NopStmtNode):
            self.visit_nop_stmt(node, code)
        elif isinstance(node, LetStmtNode):
            self.visit_let_stmt(node, code)
        elif isinstance(node, LetExprStmtNode):
            self.visit_let_expr_stmt(node, code)
        elif isinstance(node, ReturnStmtNode):
            self.visit_return_stmt(node, code)
        elif isinstance(node, ReturnExprStmtNode):
            self.visit_return_expr_stmt(node, code)
        elif isinstance(node, ScopedJumpStmt):
            self.visit_scoped_jump_stmt(node, code)
        elif isinstance(node, ExprStmtNode):
            self.visit_expr_stmt(node, code)
        elif isinstance(node, DeclNode):
            self.visit_decl(node, code)
        elif isinstance(node, IntExprNode):
            self.visit_int_expr(node, code)
        elif isinstance(node, ChrExprNode):
            self.visit_chr_expr(node, code)
        elif isinstance(node, StrExprNode):
            self.visit_str_expr(node, code)
        elif isinstance(node, IdentifierExprNode):
            self.visit_identifier_expr(node, code)
        elif isinstance(node, CallExprNode):
            self.visit_call_expr(node, code)
        elif isinstance(node, AndExprNode):
            self.visit_and_expr(node, code)
        elif isinstance(node, OrExprNode):
            self.visit_or_expr(node, code)
        elif isinstance(node, AssignExprNode):
            self.visit_assign_expr(node, code)
        elif isinstance(node, UnExprNode):
            self.visit_un_expr(node, code)
        elif isinstance(node, BinExprNode):
            self.visit_bin_expr(node, code)
        else:
            self.log_error(f"Bug: Unimplemented visitor for '{node}'!", node)
    
    
    def visit_root(self, node: RootNode, code: Code) -> None:
        """ Visit a root node. """
        
        self.scope_stack.push()
        main_label: str = code.get_label()
        
        for module in node.modules:
            self.visit(module, code)
        
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
    
    
    def visit_module(self, node: ModuleNode, code: Code) -> None:
        """ Visit a module node. """
        
        for stmt in node.stmts:
            self.visit(stmt, code)
    
    
    def visit_intrinsic_stmt(
            self, node: IntrinsicStmtNode, code: Code) -> None:
        """ Visit an intrinsic statement node. """
        
        name: str = node.name.name
        
        if self.scope_stack.has(name):
            self.log_error(
                    f"Intrinsic name '{name}' is already defined "
                    "in the current scope!",
                    node.name)
            return
        
        if name in self.intrinsics:
            parent_label: str = code.get_label()
            intrinsic_label: str = code.append_label(f"intrinsic_{name}")
            code.set_label(intrinsic_label)
            
            intrinsic: Intrinsic = self.intrinsics[name]
            intrinsic.generator(code)
            code.make_return()
            
            code.set_label(parent_label)
            self.scope_stack.define_intrinsic(
                    name, intrinsic_label, intrinsic.arity)
        else:
            self.log_error(f"Intrinsic '{name}' does not exist!", node.name)
    
    
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
            self.scope_stack.define_func(name, func_label, len(node.decls))
        
        # Buffer scope.
        self.scope_stack.push()
        self.scope_stack.undefine_locals()
        self.scope_stack.undefine_scoped_label("break")
        self.scope_stack.undefine_scoped_label("continue")
        
        # Parameter scope.
        self.scope_stack.push()
        
        for decl in node.decls:
            self.visit(decl, code)
        
        # Body scope.
        self.scope_stack.push()
        self.visit(node.stmt, code)
        code.make_push_int(0)
        code.make_return()
        self.scope_stack.pop()
        
        self.scope_stack.pop() # End parameter scope.
        self.scope_stack.pop() # End buffer scope.
        code.set_label(parent_label)
    
    
    def visit_block_stmt(self, node: BlockStmtNode, code: Code) -> None:
        """ Visit a block statement node. """
        
        self.scope_stack.push()
        
        for stmt in node.stmts:
            self.visit(stmt, code)
        
        self.pop_scope(code)
    
    
    def visit_if_stmt(self, node: IfStmtNode, code: Code) -> None:
        """ Visit an if statement node. """
        
        end_label: str = code.insert_label("if_end")
        self.visit(node.expr, code)
        code.make_jump_zero_label(end_label)
        
        self.scope_stack.push()
        self.visit(node.stmt, code)
        self.pop_scope(code)
        
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
        self.pop_scope(code)
        
        code.set_label(else_label)
        self.scope_stack.push()
        self.visit(node.else_stmt, code)
        self.pop_scope(code)
        
        code.set_label(end_label)
    
    
    def visit_while_stmt(self, node: WhileStmtNode, code: Code) -> None:
        """ Visit a while statement node. """
        
        end_label: str = code.insert_label("while_end")
        condition_label: str = code.insert_label("while_condition")
        code.set_label(condition_label)
        self.visit(node.expr, code)
        code.make_jump_zero_label(end_label)
        
        self.scope_stack.push()
        self.scope_stack.define_scoped_label("break", end_label)
        self.scope_stack.define_scoped_label("continue", condition_label)
        self.visit(node.stmt, code)
        code.make_jump_label(condition_label)
        self.pop_scope(code)
        
        code.set_label(end_label)
    
    
    def visit_nop_stmt(self, node: NopStmtNode, code: Code) -> None:
        """ Visit a no operation statement node. """
        
        pass # No operation statements should have no effect.
    
    
    def visit_let_stmt(self, node: LetStmtNode, code: Code) -> None:
        """ Visit a let statement node. """
        
        code.make_push_int(0)
        
        if self.scope_stack.has(node.decl.name):
            code.make_drop()
        
        self.visit(node.decl, code)
        
        if not node.decl.is_mutable:
            self.log_error(
                    "No value assigned "
                    f"to immutable local '{node.decl.name}'! Assign a value "
                    "or use the 'mut' keyword.", node.decl)
    
    
    def visit_let_expr_stmt(self, node: LetExprStmtNode, code: Code) -> None:
        """ Visit a let expression statement node. """
        
        self.visit(node.expr, code)
        
        if self.scope_stack.has(node.decl.name):
            code.make_drop()
        
        self.visit(node.decl, code)
    
    
    def visit_return_stmt(self, node: ReturnStmtNode, code: Code) -> None:
        """ Visit a return statement node. """
        
        code.make_push_int(0)
        code.make_return()
    
    
    def visit_return_expr_stmt(
            self, node: ReturnExprStmtNode, code: Code) -> None:
        """ Visit a return expression statement node. """
        
        self.visit(node.expr, code)
        code.make_return()
    
    
    def visit_scoped_jump_stmt(self, node: ScopedJumpStmt, code: Code) -> None:
        """ Visit a scoped jump statement node. """
        
        label: ScopedLabel = self.scope_stack.get_scoped_label(node.name)
        
        if not label.is_available:
            if node.name == "break":
                self.log_error(
                        "Cannot use 'break' outside of a while loop!", node)
            elif node.name == "continue":
                self.log_error(
                        "Cannot use 'continue' outside of a while loop!", node)
            else:
                self.log_error(
                        "Cannot jump to "
                        f"undefined scoped label '{node.name}'!", node)
            
            code.make_push_int(0)
            code.make_return()
            return
        
        for i in range(label.local_count):
            code.make_drop()
        
        code.make_jump_label(label.label)
    
    
    def visit_expr_stmt(self, node: ExprStmtNode, code: Code) -> None:
        """ Visit an expression statement node. """
        
        self.visit(node.expr, code)
        code.make_drop()
    
    
    def visit_decl(self, node: DeclNode, code: Code) -> None:
        """ Visit a declaration node. """
        
        if self.scope_stack.has(node.name):
            self.log_error(
                    f"Local name '{node.name}' is already defined "
                    "in the current scope!", node)
            return
        
        if node.is_mutable:
            self.scope_stack.define_local_mut(node.name)
        else:
            self.scope_stack.define_local(node.name)
    
    
    def visit_int_expr(self, node: IntExprNode, code: Code) -> None:
        """ Visit an integer expression node. """
        
        code.make_push_int(node.value)
    
    
    def visit_chr_expr(self, node: ChrExprNode, code: Code) -> None:
        """ Visit a character expression node. """
        
        if len(node.value) != 1:
            if node.value:
                self.log_error(
                        "Multiple characters in character literal!", node)
            else:
                self.log_error("Empty character literal!", node)
            
            code.make_push_int(0)
            return
        
        code.make_push_chr(node.value)
    
    
    def visit_str_expr(self, node: StrExprNode, code: Code) -> None:
        """ Visit a string expression node. """
        
        code.make_push_str(node.value)
    
    
    def visit_identifier_expr(
            self, node: IdentifierExprNode, code: Code) -> None:
        """ Visit an identifier expression node. """
        
        symbol: Symbol = self.scope_stack.get(node.name)
        
        if symbol.access == SymbolAccess.UNDEFINED:
            self.log_error(
                    f"Identifier '{node.name}' is undefined "
                    "in the current scope!", node)
            code.make_push_int(0)
        elif symbol.access in (SymbolAccess.INTRINSIC, SymbolAccess.FUNC):
            code.make_push_label(symbol.str_value)
        elif symbol.access == SymbolAccess.LOCAL:
            code.make_load_local_offset(symbol.int_value)
        elif symbol.access == SymbolAccess.LOCAL_MUT:
            code.make_load_local_offset(symbol.int_value)
        else:
            self.log_error(
                    "Bug: Unimplemented symbol access "
                    f"'{symbol.access.name}' at '{node.name}'!", node)
            code.make_push_int(0)
    
    
    def visit_call_expr(self, node: CallExprNode, code: Code) -> None:
        """ Visit a call expression node. """
        
        # Whether the callee can be called.
        is_callable: bool = False
        
        # Number of parameters expected. -1 for any number.
        expected_params: int = -1
        
        # Intrinsic name. Empty for non-intrinsic.
        intrinsic_name: str = ""
        
        if isinstance(node.callee, IntExprNode):
            self.log_error(
                    f"Called the integer value '{node.callee.value}' "
                    "as a function!", node.callee)
        elif isinstance(node.callee, ChrExprNode):
            self.log_error(
                    f"Called the character value '{node.callee.value}' "
                    "as a function!", node.callee)
        elif isinstance(node.callee, StrExprNode):
            self.log_error(
                    f"Called the string value '{node.callee.value}' "
                    "as a function!", node.callee)
        elif isinstance(node.callee, IdentifierExprNode):
            symbol: Symbol = self.scope_stack.get(node.callee.name)
            
            if symbol.access == SymbolAccess.UNDEFINED:
                self.log_error(
                        f"Called function name '{symbol.name}' is undefined "
                        "in the current scope!", node.callee)
            elif symbol.access == SymbolAccess.INTRINSIC:
                is_callable = True
                expected_params = symbol.int_value
                intrinsic_name = symbol.name
            elif symbol.access == SymbolAccess.FUNC:
                is_callable = True
                expected_params = symbol.int_value
            elif symbol.access == SymbolAccess.LOCAL:
                is_callable = True # A local may contain a function.
            elif symbol.access == SymbolAccess.LOCAL_MUT:
                is_callable = True
            else:
                self.log_error(
                        "Bug: Unimplemented callee symbol access "
                        f"'{symbol.access.name}' at '{node.callee}'!",
                        node.callee)
        elif isinstance(node.callee, CallExprNode):
            is_callable = True # A call may return a function.
        else:
            self.log_error("Cannot call an expression!", node.callee)
        
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
        
        if intrinsic_name:
            self.intrinsics[intrinsic_name].generator(code)
        else:
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
    
    
    def visit_assign_expr(self, node: AssignExprNode, code: Code) -> None:
        """ Visit an assign expression node. """
        
        if node.op != AssignOp.SIMPLE:
            self.visit(node.lhs_expr, code)
        
        self.visit(node.rhs_expr, code)
        
        if node.op == AssignOp.SIMPLE:
            pass # Simple assignment should not modify the value.
        elif node.op == AssignOp.ADD:
            code.make_binary_add()
        elif node.op == AssignOp.SUBTRACT:
            code.make_binary_subtract()
        elif node.op == AssignOp.MULTIPLY:
            code.make_binary_multiply()
        elif node.op == AssignOp.DIVIDE:
            code.make_binary_divide()
        elif node.op == AssignOp.MODULO:
            code.make_binary_modulo()
        elif node.op == AssignOp.AND:
            code.make_binary_and()
        elif node.op == AssignOp.OR:
            code.make_binary_or()
        else:
            self.log_error(
                    "Bug: Unimplemented "
                    f"assignment operator '{node.op.name}'!", node)
            code.make_drop() # Preserve stack size.
        
        if not isinstance(node.lhs_expr, IdentifierExprNode):
            self.log_error("Cannot assign to an expression!", node.lhs_expr)
            return
        
        name: str = node.lhs_expr.name
        symbol: Symbol = self.scope_stack.get(name)
        
        if symbol.access == SymbolAccess.UNDEFINED:
            self.log_error(
                    "Cannot assign "
                    f"to undefined name '{name}'!", node.lhs_expr)
        elif symbol.access in (SymbolAccess.INTRINSIC, SymbolAccess.FUNC):
            self.log_error(
                    f"Cannot assign to function '{name}'!", node.lhs_expr)
        elif symbol.access == SymbolAccess.LOCAL:
            self.log_error(
                    f"Cannot assign to immutable local '{name}'! "
                    f"Declare '{name}' with the 'mut' keyword.", node.lhs_expr)
        elif symbol.access == SymbolAccess.LOCAL_MUT:
            code.make_store_local_offset(symbol.int_value)
        else:
            self.log_error(
                    "Bug: Unimplemented assignment symbol access "
                    f"'{symbol.access.name}' at '{node.lhs_expr}'!",
                    node.lhs_expr)
    
    
    def visit_un_expr(self, node: UnExprNode, code: Code) -> None:
        """ Visit a unary expression node. """
        
        self.visit(node.expr, code)
        
        if node.op == UnOp.DEREFERENCE:
            code.make_unary_dereference()
        elif node.op == UnOp.AFFIRM:
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
