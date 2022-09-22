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
