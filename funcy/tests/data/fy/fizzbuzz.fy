/*
* Funcy Test Script - fizzbuzz.fy
* The classic FizzBuzz program.
*/

include "//print.fy"; // Include standard print library.

// Play FizzBuzz for (1 ... 100).
func main() {
	// Return whether a number has a factor and print a message if it does.
	func hasFactor(number, factor, message) {
		if (number % factor) {
			return false;
		}
		
		printStr(message);
		return true;
	}
	
	let mut i = 0;
	
	while (i < 100) {
		i += 1;
		
		let mut hasFactors = false;
		hasFactors |= hasFactor(i, 3, "Fizz");
		hasFactors |= hasFactor(i, 5, "Buzz");
		
		if (hasFactors) {
			putChr('!');
			putChr('\n');
		} else {
			printIntLn(i);
		}
	}
}
