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
Below is an example program written in Funcy for calculating the distance
squared between two 2D points:
```
/*
* Funcy Test Script - example.fy
* Calculates squared distances between 2D points.
*/

// Calculate the distance squared between (aX, aY) and (bX, bY).
func distanceSquared2D(aX, aY, bX, bY){
   // Return x squared.
   func sq(x){
      return x * x;
   }
   
   return sq(bX - aX) + sq(bY - aY);
}

// Entry point.
func main(){
   // Test the distance function and return whether it failed.
   func testFailed(aX, aY, bX, bY, result){
      return distanceSquared2D(aX, aY, bX, bY) != result;
   }
   
   // Run tests on our squared distance function:
   if(testFailed(0, 0, 0, 0, 0)) return 1;
   if(testFailed(123, 456, 123, 456, 0)) return 1;
   if(testFailed(0, 0, 1, 0, 1)) return 1;
   if(testFailed(0, 0, 1, 1, 2)) return 1;
   if(testFailed(0, 0, 10, 0, 100)) return 1;
   if(testFailed(5, 10, 15, 10, 100)) return 1;
   if(testFailed(2, 3, 5, 7, 25)) return 1;
   if(testFailed(0, 10, 0, -10, 400)) return 1;
   
   print(123); // Print 123 on success!
}
```

Other features include nestable comments, and passing and returning functions
as values. `true` and `false` keywords are available, but these are synonyms
for `1` and `0` as there is no type system.

# Grammar
The EBNF (Extended Backus-Naur Form) grammar for Funcy's current implementation
is as follows:
```EBNF
(* Funcy Reference Grammar *)

root = { stmt_func }, EOF ;

stmt = (
   stmt_func | stmt_block | stmt_if | stmt_while | stmt_nop |  stmt_let |
   stmt_return | stmt_print | stmt_expr
) ;

stmt_func   = "func", IDENTIFIER, "(", [ decl, { ",", decl } ], ")", stmt_block ;
stmt_block  = "{", { stmt }, "}" ;
stmt_if     = "if", expr_paren, stmt, [ "else", stmt ] ;
stmt_while  = "while", expr_paren, stmt ;
stmt_nop    = ";" ;
stmt_let    = "let", decl, [ "=", expr ], ";" ;
stmt_return = "return", [ expr ], ";" ;
stmt_print  = "print", expr_paren, ";" ;
stmt_expr   = expr, ";" ;

decl = [ "mut" ], IDENTIFIER ;

expr_paren = "(", expr, ")" ;
expr       = expr_assignment ;

(* Expressions by increasing precedence level. *)
expr_assignment  = expr_logical_or, [ ( "%=" | "&=" | "*=" | "+=" | "-=" | "/=" | "=" | "|=" ), expr_assignment ] ;
expr_logical_or  = expr_logical_and, { "||", expr_logical_and } ;
expr_logical_and = expr_eager_or, { "&&", expr_eager_or } ;
expr_eager_or    = expr_eager_and, { "|", expr_eager_and } ;
expr_eager_and   = expr_equality, { "&", expr_equality } ;
expr_equality    = expr_comparison, { ( "!=" | "==" ), expr_comparison } ;
expr_comparison  = expr_sum, { ( "<" | "<=" | ">" | ">=" ), expr_sum } ;
expr_sum         = expr_term, { ( "+" | "-" ), expr_term } ;
expr_term        = expr_prefix, { ( "%" | "*" | "/" ), expr_prefix } ;
expr_prefix      = ( "!" | "+" | "-" ), expr_prefix | expr_call ;
expr_call        = expr_primary, { "(", [ expr, { ",", expr } ], ")" } ;
expr_primary     = expr_paren | LITERAL_INT | IDENTIFIER | "false" | "true" ;
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
