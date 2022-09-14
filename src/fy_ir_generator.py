from fy_ir_code import IRCode
from fy_node import Node
from fy_node_decl_func import FuncDeclNode
from fy_node_expr_int import IntExprNode
from fy_node_program import ProgramNode
from fy_node_stmt_compound import CompoundStmtNode
from fy_node_stmt_expr import ExprStmtNode
from fy_node_stmt_expr_print import PrintExprStmtNode
from fy_node_stmt_nop import NopStmtNode
from fy_scope_stack import ScopeStack
from fy_scope_symbol import ScopeSymbol
from fy_scope_symbol_type import ScopeSymbolType

class IRGenerator:
    """ Generates IR code from an abstract syntax tree. """
    
    has_errors: bool = False
    """ Whether errors were encountered while generating IR code. """
    
    def generate(self, ast: ProgramNode) -> IRCode:
        """ Generate IR code from an abstract syntax tree. """
        
        self.has_errors = False
        code: IRCode = IRCode()
        self.visit(ast, ScopeStack(), code)
        return code
    
    
    def log_error(self, message: str) -> None:
        """ Log an error message. """
        
        print(f"Error: {message}")
        self.has_errors = True
    
    
    def visit(self, node: Node, scope: ScopeStack, code: IRCode) -> None:
        """ Visit an AST node. """
        
        if isinstance(node, ProgramNode):
            self.visit_program(node, scope, code)
        elif isinstance(node, FuncDeclNode):
            self.visit_func_decl(node, scope, code)
        elif isinstance(node, CompoundStmtNode):
            self.visit_compound_stmt(node, scope, code)
        elif isinstance(node, NopStmtNode):
            self.visit_nop_stmt(node, scope, code)
        elif isinstance(node, ExprStmtNode):
            self.visit_expr_stmt(node, scope, code)
        elif isinstance(node, IntExprNode):
            self.visit_int_expr(node, scope, code)
        else:
            print(f"Codegen bug: Unimplemented visitor for '{node}'!")
    
    
    def visit_program(self, node: ProgramNode, scope: ScopeStack, code: IRCode) -> None:
        """ Visit a program node. """
        
        scope.push_scope()
        main_label: str = code.get_label()
        
        for func_decl in node.func_decls:
            self.visit(func_decl, scope, code)
        
        code.set_label(main_label)
        symbol: ScopeSymbol = scope.get_symbol("main")
        
        if symbol.type == ScopeSymbolType.LABEL:
            for i in range(symbol.int_value):
                code.make_push_int(0)
            
            code.make_push_label(symbol.str_value)
            code.make_call_argc(symbol.int_value)
        else:
            code.make_push_int(0)
        
        code.make_halt()
        scope.pop_scope()
    
    
    def visit_func_decl(self, node: FuncDeclNode, scope: ScopeStack, code: IRCode) -> None:
        """ Vist a function declaration node. """
        
        if scope.has_symbol(node.name):
            self.log_error(f"Function name '{node.name}' is already defined!")
            return
        
        tail_label: str = code.insert_label(f"func_tail_{node.name}")
        body_label: str = code.insert_label(f"func_body_{node.name}")
        code.set_label(body_label)
        scope.define_label(node.name, body_label, len(node.params))        
        scope.push_scope()
        scope.undefine_locals()
        scope.push_scope()
        
        for param in node.params:
            if scope.has_symbol(param):
                self.log_error(
                        f"Parameter '{param}' is already defined in {node.name}'s parameter list!")
            else:
                scope.define_local(param)
        
        scope.push_scope()
        self.visit(node.stmt, scope, code)
        scope.pop_scope()
        scope.pop_scope()
        scope.pop_scope()
        code.set_label(tail_label)
        code.make_push_int(0)
        code.make_return()
    
    
    def visit_compound_stmt(self, node: CompoundStmtNode, scope: ScopeStack, code: IRCode) -> None:
        """ Visit a compound statement node. """
        
        scope.push_scope()
        
        for stmt in node.stmts:
            self.visit(stmt, scope, code)
        
        scope.pop_scope()
    
    
    def visit_nop_stmt(self, node: NopStmtNode, scope: ScopeStack, code: IRCode) -> None:
        """ Visit a no operation statement node. """
        
        code.make_no_operation()
    
    
    def visit_expr_stmt(self, node: ExprStmtNode, scope: ScopeStack, code: IRCode) -> None:
        """ Visit an expression statement node. """
        
        self.visit(node.expr, scope, code)
        
        if isinstance(node, PrintExprStmtNode):
            self.visit_print_expr_stmt(node, scope, code)
        else:
            code.make_discard()
    
    
    def visit_print_expr_stmt(
            self, node: PrintExprStmtNode, scope: ScopeStack, code: IRCode) -> None:
        """ Visit a print expression statement node. """
        
        code.make_print()
    
    
    def visit_int_expr(self, node: IntExprNode, scope: ScopeStack, code: IRCode) -> None:
        """ Visit an integer expression node. """
        
        code.make_push_int(node.value)
