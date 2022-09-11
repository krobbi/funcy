from fy_node_stmt import StmtNode

class CompoundStmtNode(StmtNode):
    """ A compound statement node of an abstract syntax tree. """
    
    stmts: list[StmtNode]
    """ The compound statement's statements. """
    
    def __init__(self) -> None:
        """ Initialize the compound statement's statements. """
        
        super().__init__()
        self.stmts = []
    
    
    def __repr__(self) -> str:
        """ Return the compound statement's string representation. """
        
        return "CompoundStmt"
    
    
    def get_children(self) -> list[StmtNode]:
        """ Get the compound statement's children as a list. """
        
        return self.stmts
