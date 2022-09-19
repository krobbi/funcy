def test_repl() -> None:
    """ Test the Funcy REPL. """
    
    from ..repl import repl
    
    repl()


if __name__ == "__main__" and __package__ == "funcy.tests":
    test_repl()
