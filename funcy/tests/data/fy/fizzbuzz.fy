/*
* Funcy Test Script - fizzbuzz.fy
* The classic FizzBuzz program. Adapted for the very limited feature set.
*/

// Get whether x and y are equal.
func isEqual(x, y){
	if(x - y){
		// If one value minus another is non-zero, they must not be equal.
		return 0;
	}
	
	return 1;
}

/*
* Play FizzBuzz with a single number. Print 300, 1000 if it is a multiple of 3,
* print 500, 1000 if it is a multiple of 5, print 300, 500, 1000 if it is a
* multiple of both 3 and 5. Otherwise, print the number itself.
*/
func fizzBuzz(number){
	/*
	* Get whether a number is a multiple of a factor, and print a message number
	* if it is.
	*/
	func tryFactor(number, factor, message){
		if(isEqual(number % factor, 0)){
			print(message);
			return 1;
		}
		
		return 0;
	}
	
	if(
		tryFactor(number, 3, 300) +
		tryFactor(number, 5, 500)
	){
		// If any test succeeds, print the ending '1000' message and return.
		print(1000);
		return;
	}
	
	print(number); // Print the number itself if no tests succeeded.
}

// FizzBuzz implementation.
func main(){
	// Call a function with a parameter for every number in a range.
	func loop(min, max, f){
		f(min); // The minimum value doubles as the loop counter.
		
		if(isEqual(min, max)){
			return; // Stop the loop if we have reached the maximum.
		}
		
		loop(min + 1, max, f); // Run another loop. There is no loop statement.
	}
	
	loop(1, 100, fizzBuzz); // Play FizzBuzz for (1 ... 100).
}
