/*
* Funcy Test Script - fizzbuzz.fy
* The classic FizzBuzz program. Adapted for the very limited feature set.
*/

/*
* Play FizzBuzz with a single number. Print 'Fizz!' if it is a multiple of 3,
* print 'Buzz!' if it is a multiple of 5, or print 'FizzBuzz!' if it is a
* multiple of both 3 and 5. Otherwise, print the number itself.
*/
func fizzBuzz(number){
	/*
	* Get whether a number is a multiple of a factor, and print a message if it
	* is.
	*/
	func tryFactor(number, factor, mut message){
		if(number % factor){
			return false;
		}
		
		let base = 256;
		let mut magnitude = base;
		
		while(magnitude <= message){
			magnitude *= base;
		}
		
		while(magnitude >= base){
			magnitude /= base;
			let character = message / magnitude;
			message -= character * magnitude;
			putChr(character);
		}
		
		return true;
	}
	
	let mut hasFactor = false;
	hasFactor |= tryFactor(number, 3, 0x46_69_7a_7a); // 'Fizz'.
	hasFactor |= tryFactor(number, 5, 0x42_75_7a_7a); // 'Buzz'.
	
	if(hasFactor){
		putChr(0x21); // '!'.
		putLn();
	}else{
		printIntLn(number);
	}
}

// FizzBuzz implementation.
func main(){
	let mut i = 0;
	
	while(i < 100){
		fizzBuzz(i += 1);
	}
}
