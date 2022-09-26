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
