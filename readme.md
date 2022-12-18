# Funcy
_A toy functional language written in Python._  
__Copyright &copy; 2022 Chris Roberts__ (Krobbizoid).

# Contents
1. [About](#about)
2. [Example](#example)
   1. [Standard Library](#standard-library)
		1. [`//math.fy`](#mathfy)
		2. [`//print.fy`](#printfy)
		3. [`//std.fy`](#stdfy)
   2. [About Strings](#about-strings)
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
Below is a FizzBuzz program written in Funcy:
```
/*
* Funcy Test Script - fizzbuzz.fy
* The classic FizzBuzz program.
*/

include "//print.fy"; // Include standard print library.

// Play FizzBuzz for (1 ... 100).
func main(){
	// Return whether a number has a factor and print a message if it does.
	func hasFactor(number, factor, message){
		if(number % factor){
			return false;
		}
		
		printStr(message);
		return true;
	}
	
	let mut i = 0;
	
	while(i < 100){
		i += 1;
		
		let mut hasFactors = false;
		hasFactors |= hasFactor(i, 3, "Fizz");
		hasFactors |= hasFactor(i, 5, "Buzz");
		
		if(hasFactors){
			printChrLn('!');
		} else {
			printIntLn(i);
		}
	}
}
```

Please note that Funcy does not yet have a type system. All values are handled
as integers.

## Standard Library
The following standard libraries are available to all Funcy programs. To
include a standard library, include a path starting with a double slash, e.g.
`include "//std.fy";`.

### `//math.fy`
A library of functions for mathematical operations.

| Function      | Description                                                                 |
| :------------ | :-------------------------------------------------------------------------- |
| `abs(value)`  | Return an integer's absolute value.                                         |
| `sign(value)` | Return an integer's sign as zero (`0`), positive (`1`), or negative (`-1`). |
| `min(x, y)`   | Return the minimum of two integers.                                         |
| `max(x, y)`   | Return the maximum of two integers.                                         |

### `//print.fy`
A library of functions for printing values.

| Function                      | Description                                                                                                     |
| :---------------------------- | :-------------------------------------------------------------------------------------------------------------- |
| `getDigitChr(digit)`          | Get a digit's character. E.g. `5` -> `'5'`, `10` -> `'a'`.                                                      |
| `putChr(character)`           | Put a character to the standard output and return it.                                                           |
| `putLn()`                     | Put a line break to the standard output and return it.                                                          |
| `printLn()`                   | Print a line break and return the number of printed characters.                                                 |
| `printChr(character)`         | Print a character and return the number of printed characters.                                                  |
| `printChrLn(character)`       | Print a character with a line break and return the number of printed characters.                                |
| `printStr(string)`            | Print a string and return the number of printed characters.                                                     |
| `printStrLn(string)`          | Print a string with a line break and return the number of printed characters.                                   |
| `printIntBase(value, base)`   | Print an integer with a base between `2` and `36` and return the number of printed characters.                  |
| `printIntBaseLn(value, base)` | Print an integer with a base between `2` and `36` and a line break and return the number of printed characters. |
| `printInt(value)`             | Print an integer and return the number of printed characters.                                                   |
| `printIntLn(value)`           | Print an integer with a line break and return the number of printed characters.                                 |

### `//std.fy`
A library of all available standard functions.

Includes:
* `//math.fy`
* `//print.fy`

| Function         | Description                                                                                      |
| :--------------- | :----------------------------------------------------------------------------------------------- |
| `lenStr(string)` | Return the length of a string excluding the null terminator.                                     |
| `cmpStr(x, y)`   | Compare two strings as greater (`> 0`), lesser (`< 0`), or equal (`== 0`) when sorted lexically. |
| `eqStr(x, y)`    | Return whether two strings are equal.                                                            |

## About Strings
Strings in Funcy are much like strings in C as in they don't really exist. A
string is just a pointer to its first character. Working with strings may give
you unexpected results. Two strings with the same content may not have the same
address, and thus may not be equal. Due to the lack of typing, adding two
strings will give you the sum of their addresses, and not a concatenated
string. The lack of writable memory in the FVM outside of the stack means that
string manipulation features are not yet feasible.

# Grammar
The EBNF (Extended Backus-Naur Form) grammar for Funcy's current implementation
is as follows:
```EBNF
(* Funcy Reference Grammar *)

module = { incl }, { stmt_func }, EOF ;

incl = "include", LITERAL_STR, ";" ;

stmt = (
   stmt_func | stmt_block | stmt_if | stmt_while | stmt_nop |  stmt_let |
   stmt_return | stmt_break | stmt_continue | stmt_expr
) ;

stmt_func     = "func", IDENTIFIER, "(", [ decl, { ",", decl } ], ")", stmt_block ;
stmt_block    = "{", { stmt }, "}" ;
stmt_if       = "if", expr_paren, stmt, [ "else", stmt ] ;
stmt_while    = "while", expr_paren, stmt ;
stmt_nop      = ";" ;
stmt_let      = "let", decl, [ "=", expr ], ";" ;
stmt_return   = "return", [ expr ], ";" ;
stmt_break    = "break", ";" ;
stmt_continue = "continue", ";" ;
stmt_expr     = expr, ";" ;

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
expr_prefix      = ( "!" | "*" | "+" | "-" ), expr_prefix | expr_call ;
expr_call        = expr_primary, { "(", [ expr, { ",", expr } ], ")" } ;
expr_primary     = expr_paren | expr_intrinsic | LITERAL_INT | LITERAL_CHR | LITERAL_STR | IDENTIFIER | "false" | "true" ;

(* Secret expression type limited to the standard library. *)
expr_intrinsic = "$(", IDENTIFIER, { ",", expr }, ")" ;
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
