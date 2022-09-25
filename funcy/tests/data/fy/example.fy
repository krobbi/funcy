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
func getGetMagic(foo, bar){
   // Functions may be nested inside of other functions to limit their scope.
   func getMagic(){
      /*
      * All functions return a value, but the value or even the entire return
      * statement may be omitted.
      */
      return 123;
   }
   
   // Functions may be passed to and returned from other functions.
   return getMagic;
}

/*
* If a function named 'main' exists, it will be used as the entry point for the
* program. Any parameters given to 'main' will always be '0' in the current
* implementation.
*/
func main(){
   /*
   * In the current implementation, 'print' is a keyword, and not the name of a
   * standard function. The print statement expects parentheses. Strings are
   * unavailable in the current implementation, so '123' is printed instead of
   * a hello world message. Function calls are also checked for the correct
   * parameter count.
   */
   print(getGetMagic(1, 2)());
   
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
}
