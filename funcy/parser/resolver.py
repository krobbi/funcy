from enum import Enum, auto
from pathlib import Path

from ..ast.nodes import ModuleNode, RootNode
from ..io.input_wrapper import InputWrapper
from ..io.log import Log
from .parser import Parser

class ResolverModuleState(Enum):
    """ The state of a resolver module. """
    
    UNPARSED = auto()
    """ Module is declared but not yet parsed. """
    
    PARSED = auto()
    """ Module has been declared and parsed. """
    
    VISITED = auto()
    """ Module has been visited by the resolver. """
    
    RESOLVED = auto()
    """ Module has been resolved. """


class ResolverModule:
    """ A module to be resolved by the resolver. """
    
    state: ResolverModuleState = ResolverModuleState.UNPARSED
    """ The resolver module's state. """
    
    ast: ModuleNode
    """ The resolver module's AST. """
    
    def __init__(self) -> None:
        """ Initialize the resolver module's AST. """
        
        self.ast = ModuleNode()


class Resolver:
    """ Resolves a Funcy program's dependencies. """
    
    BAD_PATH_CHARS: str = '"*/:<>?\\|'
    """ Characters not allowed in paths. """
    
    log: Log
    """ The resolver's log. """
    
    parser: Parser
    """ The resolver's parser. """
    
    root_dir: str = ""
    """ The absolute path of the Funcy program's root directory. """
    
    modules: dict[str, ResolverModule]
    """ The Funcy program's modules. """
    
    def __init__(self, log: Log) -> None:
        """ Initialize the resolver's log, parser, and modules. """
        
        self.log = log
        self.parser = Parser(self.log)
        self.modules = {}
    
    
    def get_module_name(self, name: str, path: str):
        """
        Get a module's name from its parent module's name and include
        path. Return an empty string if the include path is invalid.
        """
        
        is_abs: bool = False # Paths starting with '/' are absolute.
        is_std: bool = name.startswith("//")
        
        path = path.strip().replace("\\", "/")
        
        if path.startswith("//"):
            is_abs = True
            is_std = True
            path = path[2:].lstrip()
        elif path.startswith("/"):
            is_abs = True
            path = path[1:].lstrip()
        
        # Don't allow empty path parts.
        if "//" in path or path.startswith("/") or path.endswith("/"):
            return ""
        
        path_parts: list[str] = [] if is_abs else name.split("/")[:-1]
        
        for part in path.split("/"):
            part = part.strip() # Don't allow surrounding whitespace.
            
            if not part: # Don't allow whitespace-only path parts.
                return ""
            elif part == ".": # Single dot means same directory.
                continue
            elif part == "..": # Double dot means parent directory.
                if not path_parts: # Don't ascend beyond root.
                    return ""
                
                path_parts.pop()
            elif part.endswith("."): # Don't allow trailing dots.
                return ""
            else:
                for character in part: # Don't allow illegal characters.
                    if(
                            ord(character) < 32 or ord(character) == 127
                            or character in self.BAD_PATH_CHARS):
                        return ""
                
                path_parts.append(part)
        
        return ("//" if is_std else "") + "/".join(path_parts)
    
    
    def get_module_path(self, name: str) -> str:
        """ Get a module's absolute path from its name. """
        
        if name.startswith("//"):
            return str(Path(__file__).parent.joinpath(
                    f"../std/{name[2:]}").resolve())
        
        return str(Path(self.root_dir).joinpath(name).resolve())
    
    
    def set_module_state(self, name: str, state: ResolverModuleState) -> None:
        """ Set a module's state from its name. """
        
        if name in self.modules:
            self.modules[name].state = state
    
    
    def get_module_state(self, name: str) -> ResolverModuleState:
        """ Get a module's state from its name. """
        
        # Return early if the module does not exist.
        if not name in self.modules:
            return ResolverModuleState.UNPARSED
        
        return self.modules[name].state
    
    
    def get_module_ast(self, name) -> ModuleNode:
        """ Get a module's AST from its name. """
        
        # Return early if the module does not exist.
        if not name in self.modules:
            return ModuleNode()
        
        return self.modules[name].ast
    
    
    def get_module_children(self, name: str) -> list[str]:
        """ Get a module's child module names from its name. """
        
        ast: ModuleNode = self.get_module_ast(name)
        children: list[str] = []
        
        for include_node in ast.incls:
            child: str = self.get_module_name(name, include_node.name)
            
            if not child:
                self.log.log(
                        f"Illegal include path '{include_node.name}'!",
                        include_node.span)
            elif child == name:
                self.log.log("Module includes itself!", include_node.span)
            elif child in children:
                self.log.log(
                        f"Module '{child}' is already included!",
                        include_node.span)
            elif self.get_module_state(child) == ResolverModuleState.VISITED:
                self.log.log(
                        f"Including module '{child}' creates "
                        "a circular dependency!", include_node.span)
            else:
                children.append(child)
        
        return children
    
    
    def declare_module(self, name: str) -> None:
        """
        Declare and parse a module from its name if it is not available.
        """
        
        if not name in self.modules:
            self.modules[name] = ResolverModule()
        
        module: ResolverModule = self.modules[name]
        
        if module.state != ResolverModuleState.UNPARSED:
            return
        
        wrapper: InputWrapper = InputWrapper()
        wrapper.from_path(self.get_module_path(name))
        
        if wrapper.is_ok and not wrapper.is_binary:
            module.ast = self.parser.parse_module(name, wrapper.source)
        else:
            self.log.log(f"Failed to load module '{name}'!")
        
        module.state = ResolverModuleState.PARSED
    
    
    def declare_module_source(self, name: str, source: str) -> None:
        """
        Declare and parse a module from its name and source if it is not
        available.
        """
        
        if not name in self.modules:
            self.modules[name] = ResolverModule()
        
        module: ResolverModule = self.modules[name]
        
        if module.state != ResolverModuleState.UNPARSED:
            return
        
        module.ast = self.parser.parse_module(name, source)
        module.state = ResolverModuleState.PARSED
    
    
    def resolve_path(self, path: str) -> RootNode:
        """
        Resolve a Funcy program's AST from its main module's path.
        """
        
        root_node: RootNode = RootNode()
        global_path: Path = Path().joinpath(path).resolve()
        
        if not global_path.is_file():
            self.log.log("Program must be parsed from a file path!")
            return root_node
        
        self.root_dir = str(global_path.parent)
        self.modules = {}
        
        main_module_name: str = self.get_module_name(
                global_path.name, global_path.name)
        
        if not main_module_name:
            self.log.log("Illegal name for main module file!")
            return root_node
        
        self.visit_module(main_module_name, root_node)
        return root_node
    
    
    def resolve_source(self, source: str) -> RootNode:
        """ Resolve a Funcy program's AST from its source code. """
        
        root_node: RootNode = RootNode()
        self.root_dir = str(Path().resolve())
        self.modules = {}
        self.declare_module_source("<source>", source)
        self.visit_module("<source>", root_node)
        return root_node
    
    
    def visit_module(self, name: str, root_node: RootNode) -> None:
        """ Visit and resolve a module from its name. """
        
        self.declare_module(name)
        
        # Return early if the module has already been visited.
        if self.get_module_state(name) != ResolverModuleState.PARSED:
            return
        
        self.set_module_state(name, ResolverModuleState.VISITED)
        
        for child in self.get_module_children(name):
            self.visit_module(child, root_node)
        
        root_node.modules.append(self.get_module_ast(name))
        self.set_module_state(name, ResolverModuleState.RESOLVED)
