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
* parameter names in parentheses, and a function body in a block statement. In
* the current implementation, functions are not callable and their parameters
* can't be used.
*/
func foo(bar, baz){
   func qux(){} // Functions may be nested inside of other functions.
}

/*
* If a function named 'main' exists, it will be used as the entry point for the
* program. Any parameters given to 'main' will always be '0' in the current
* implementation.
*/
func main(){
   /*
   * In the current implementation, 'print' is a keyword, and not the name of a
   * standard function. The print statement expects parentheses. Only integers
   * and function identifiers are available in the current implementation, so
   * '123' is printed instead of a hello world message.
   */
   print(123);
   
   print(foo); // We can also use the addresses of functions.
   
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
}
