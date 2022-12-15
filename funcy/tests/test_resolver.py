def test_resolver() -> None:
    """ Test the resolver. """
    
    from ..ast.utils import print_ast
    from ..io.log import Log
    from ..parser.resolver import Resolver
    
    log: Log = Log()
    resolver: Resolver = Resolver(log)
    print_ast(resolver.resolve_path("funcy/tests/data/fy/resolver/main.fy"))
    
    if log.has_records():
        log.print_records()


if __name__ == "__main__" and __package__ == "funcy.tests":
    test_resolver()
