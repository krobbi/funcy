/*
* Funcy Test Script - fizzbuzz.fy
* The classic FizzBuzz program. Adapted for the very limited feature set.
*/

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
		if(number % factor == 0){
			print(message);
			return true;
		} else {
			return false;
		}
	}
	
	let mut hasFactor = false;
	hasFactor |= tryFactor(number, 3, 300);
	hasFactor |= tryFactor(number, 5, 500);
	
	if(hasFactor){
		print(1000); // Print the ending '1000' message if any factors matched.
	}else{
		print(number);
	}
}

// FizzBuzz implementation.
func main(){
	let mut i = 0;
	
	while(i < 100){
		fizzBuzz(i += 1);
	}
}
