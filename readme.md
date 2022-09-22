# Funcy
_A toy functional language written in Python._  
__Copyright &copy; 2022 Chris Roberts__ (Krobbizoid).

# Contents
1. [About](#about)
2. [Example](#example)
3. [Grammar](#grammar)
4. [Runtime](#runtime)
5. [License](#license)

# About
Funcy is a toy functional language written in Python. It is developed as an
exercise to test implementing functions in an interpreted language. It is _not_
suitable as a practical language, or as a guide for creating a programming
language.

Due to its unweildy structure, Funcy is being ported from `src/` to a correctly
formatted package in `funcy/`. To test the new implementation, use
`python -m funcy.tests.test_repl` in the root directory of this repository.

The `src/` directory will be deleted after the new implementation reaches
feature parity.

# Example
Below is a 'hello world' program written in Funcy that demonstrates the feature
set for its initial implementation. The initial implementation is only useful
for printing a fixed sequence of integers:
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
* parameter names in parentheses, and a function body in a compound statement.
* In the current implementation, functions are not callable and their
* parameters can't be used.
*/
func foo(bar, baz){}

/*
* If a function named 'main' exists, it will be used as the entry point for the
* program.
*/
func main(){
   /*
   * In the initial implementation, 'print' is a keyword, and not the name of
   * a standard function. In this example, '(123)' is actually a parenthetical
   * expression. Only integers and function identifiers are available in the
   * current implementation, so '123' is printed instead of a hello world
   * message.
   */
   print(123);
   
   /*
   * Curly braces mark compound statements that contain 0 or more statements
   * in their own scope.
   */
   {
      /*
      * A statement may contain a standalone expression. No operations are
      * available in the current implementation.
      */
      456;
      
      ; // A semicolon on its own marks a no operation statement.
   }
}
```

# Grammar
The EBNF (Extended Backus-Naur Form) grammar for Funcy's current implementation
is as follows:
```EBNF
(* Funcy Reference Grammar *)

root = { stmt_func }, EOF ;

stmt = stmt_func | stmt_block | stmt_nop | stmt_print | stmt_expr ;

stmt_func  = "func", IDENTIFIER, "(", [ IDENTIFIER, { ",", IDENTIFIER } ], ")", stmt_block ;
stmt_block = "{", { stmt }, "}" ;
stmt_nop   = ";" ;
stmt_print = "print", expr_paren, ";" ;
stmt_expr  = expr, ";" ;

expr_paren = "(", expr, ")" ;
expr       = expr_primary ;

expr_primary = expr_paren | LITERAL_INT | IDENTIFIER ;
```

# Runtime
For runtime, Funcy targets the Funcy Virtual Machine (FVM), a stack-based
bytecode interpreter.

See [fvm.md](./fvm.md) for specification details.

# License
Funcy is released under the MIT License:  
https://krobbi.github.io/license/2022/mit.txt

See [license.txt](./license.txt) for a full copy of the license text.
