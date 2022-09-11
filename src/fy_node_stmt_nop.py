from fy_node_stmt import StmtNode

class NopStmtNode(StmtNode):
    """ A no operation statement node of an abstract syntax tree. """
    
    def __repr__(self) -> str:
        """ Return the no operation statement's string representation. """
        
        return "NopStmt"
