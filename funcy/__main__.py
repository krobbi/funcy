if __name__ == "__main__":
    import sys
    
    exit_code: int = 1
    
    if __package__:
        from .cli import cli
        
        exit_code = cli(sys.argv[1:])
    else:
        print("The Funcy CLI must be run as a module! Use 'python -m funcy'")
    
    sys.exit(exit_code)
