from .core import build, exec_path

def cli(args: list[str]) -> int:
    """ Run the Funcy CLI (Command Line Interface). """
    
    if not args:
        print("Funcy CLI Usage:")
        print("  'python -m funcy <subcommand>'\n")
        print("  Subcommands:")
        print("    'build <in> <out>' - Build to code at <in> to <out>.")
        print("    'run <path>' - Run the code at <path>.")
        return 1
    
    subcommand: str = args.pop(0)
    
    if subcommand == "build":
        if len(args) != 2:
            print("Expected input and output path arguments!")
            return 1
        
        build(args[0], args[1])
        return 0
    elif subcommand == "run":
        if len(args) != 1:
            print("Expected a path argument!")
            return 1
        
        return exec_path(args[0])
    else:
        print(f"Invalid subcommand '{subcommand}'!")
        return 1
