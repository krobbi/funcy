# Funcy
_A toy functional language written in Python._  
__Copyright &copy; 2022 Chris Roberts__ (Krobbizoid).

# Contents
1. [About](#about)
2. [Example](#example)
3. [Grammar](#grammar)
4. [Runtime](#runtime)
5. [Python SDK](#python-sdk)
   1. [FVM Example](#fvm-example)
   2. [Command Line Interface](#command-line-interface)
6. [License](#license)

# About
Funcy is a toy functional language written in Python. It is developed as an
exercise to test implementing functions in an interpreted language. It is _not_
suitable as a practical language, or as a guide for creating a programming
language.

# Example
Below is an example program written in Funcy that demonstrates the feature set
for its current implementation. The current implementation is only useful for
printing a fixed sequence of integers:
```
/*
* Funcy uses C-like line and block comments. Funcy source code files should be
* named with the file extension '.fy'.
*
* /*
* * Block comments may be nested inside of other block comments.
* */
*/

/*
* A Funcy program contains 0 or more top-level function declarations. These
* begin with the 'func' keyword and a function name, followed by a list of
* parameter names in parentheses, and a function body in a block statement.
*/
func getGetMagic(foo, bar){
   // Functions may be nested inside of other functions to limit their scope.
   func getMagic(){
      return 123;
   }
   
   return getMagic; // A function may return another function.
}

// Functions may be passed as parameters to other functions.
func doTwice(f, x){
   f(x);
   f(x);
   
   // Return statements may omit their value. By default this returns 0.
   return;
}

func say(message){
   /*
   * In the current implementation, 'print' is a keyword, and not the name of
   * an intrinsic function. The print statement still expects parentheses.
   * Strings are not yet available.
   */
   print(message);
   
   // Return statements may be entirely omitted. This also returns 0.
}

/*
* If a function named 'main' exists, it will be used as the entry point for the
* program. Any parameters given to 'main' will always be '0' in the current
* implementation.
*/
func main(){
   // Function calls are checked for parameter count.
   doTwice(say, getGetMagic(1, 2)());
   
   print(main); // We can use a function's name to get its address.
   
   /*
   * Curly braces mark block statements that contain 0 or more statements in
   * their own scope.
   */
   {
      /*
      * A statement may be a standalone expression followed by a semicolon. No
      * operations are available in the current implementation.
      */
      456;
      
      ; // A semicolon on its own marks a no operation statement.
   }
   
   /*
   * Any value returned from 'main' will be used as an exit code. This return
   * statement may also be omitted.
   */
   return 0;
}
```

# Grammar
The EBNF (Extended Backus-Naur Form) grammar for Funcy's current implementation
is as follows:
```EBNF
(* Funcy Reference Grammar *)

root = { stmt_func }, EOF ;

stmt = stmt_func | stmt_block | stmt_nop | stmt_return | stmt_print | stmt_expr ;

stmt_func   = "func", IDENTIFIER, "(", [ IDENTIFIER, { ",", IDENTIFIER } ], ")", stmt_block ;
stmt_block  = "{", { stmt }, "}" ;
stmt_nop    = ";" ;
stmt_return = "return", [ expr ], ";" ;
stmt_print  = "print", expr_paren, ";" ;
stmt_expr   = expr, ";" ;

expr_paren = "(", expr, ")" ;
expr       = expr_call ;

(* Expressions by increasing precedence level. *)
expr_call    = expr_primary, { "(", [ expr, { ",", expr } ], ")" } ;
expr_primary = expr_paren | LITERAL_INT | IDENTIFIER ;
```

# Runtime
For runtime, Funcy targets the Funcy Virtual Machine (FVM), a stack-based
bytecode interpreter.

See [fvm.md](./fvm.md) for specification details.

# Python SDK
The `funcy` package in this repository acts as an SDK for building Funcy source
code and executing Funcy source code and FVM bytecode. The package also
provides an FVM implementation and a command line interface.

The following methods are available to the package:
```Python
import funcy

# Run the Funcy CLI. See below for more information.
my_exit_code: int = funcy.cli(["run", "input.fy"])

# Run the Funcy REPL. Mostly used internally for testing.
funcy.repl()

# Compile Funcy code from an input file to an output file.
funcy.build("input.fy", "output.fyc")

# Compile Funcy source code to FVM bytecode.
my_bytecode: bytes = funcy.compile("func main(){}")

# Compile Funcy source code to FVM bytecode from a path.
my_other_bytecode: bytes = funcy.compile_path("input.fy")

# Execute Funcy source code or FVM bytecode.
fvm_exit_code_a: int = funcy.exec("func main(){}")
fvm_exit_code_b: int = funcy.exec(my_bytecode)

# Execute Funcy source code or FVM bytecode from a path.
fvm_exit_code_c: int = funcy.exec_path("input.fy")
fvm_exit_code_d: int = funcy.exec_path("output.fyc")
```

## FVM Example
The `FVM` class is used internally by the package, but may also be used to
implement your own FVM instance with finer control:
```Python
from funcy import FVM

def my_function(my_bytecode: bytes) -> int:
   fvm: FVM = FVM()
   
   # Use 'load_flat' to load headerless bytecode.
   if not fvm.load(my_bytecode):
      return 1 # Failed to load bytecode.
   
   if not fvm.begin():
      return 1 # FVM already running.
   
   # While the FVM's execution flag is set (i.e. running).
   while fvm.ef:
      fvm.step() # Run one instruction.
   
   return fvm.ec # Return exit code.
```

## Command Line Interface
Python can run the package as a module using `python -m funcy <subcommand>`.
This is identical to the `funcy.cli` method, but accessible from the command
line.

The following subcommands are available:
* `build <in> <out>` - Build the code at `<in>` to `<out>`.
* `run <path>` - Run the code at `<path>`.

Examples:
* `python -m funcy build input.fy output.fyc`
* `python -m funcy run input.fy`
* `python -m funcy run output.fyc`

Both Funcy source code and FVM bytecode can be run from the command line
interface.

# License
Funcy is released under the MIT License:  
https://krobbi.github.io/license/2022/mit.txt

See [license.txt](./license.txt) for a full copy of the license text.
