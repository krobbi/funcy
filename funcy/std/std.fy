/*
* Funcy Standard Library
* A library of all available standard functions.
*/

include "//math.fy";

// Put a character to the standard output and return it.
func putChr(character){
	return $(putChr, character);
}

// Put and return a line break.
func putLn(){
	return putChr('\n');
}

// Get a digit's character. E.g. 5 -> '5', 10 -> 'a'.
func getDigitChr(digit){
	if(digit < 10){
		return digit + '0';
	} else {
		return digit + 'a' - 10;
	}
}

/*
* Print an integer with a base between 2 and 36 and return the number of
* printed characters.
*/
func printIntBase(mut value, base){
	if(base < 2 | base > 36){
		return 0;
	}
	
	let mut chrCount = 0; // Number of printed characters.
	
	if(value < 0){
		value = -value;
		putChr('-');
		chrCount = 1;
	}
	
	let mut magnitude = base;
	
	while(magnitude <= value){
		magnitude *= base;
	}
	
	while(magnitude >= base){
		magnitude /= base;
		let digit = value / magnitude;
		value -= digit * magnitude;
		putChr(getDigitChr(digit));
		chrCount += 1;
	}
	
	return chrCount;
}

/*
* Print an integer with a base between 2 and 36 and a line break and
* return the number of printed characters.
*/
func printIntBaseLn(value, base){
	let chrCount = printIntBase(value, base) + 1;
	putLn();
	return chrCount;
}

// Print an integer and return the number of printed characters.
func printInt(value){
	return printIntBase(value, 10);
}

/*
* Print an integer with a line break and return the number of printed
* characters.
*/
func printIntLn(value){
	let chrCount = printIntBase(value, 10) + 1;
	putLn();
	return chrCount;
}

// Print a character and return the number of printed characters.
func printChr(value){
	if(value){
		putChr(value);
		return 1;
	} else {
		return 0;
	}
}

/*
* Print a character with a line break and return the number of printed
* characters.
*/
func printChrLn(value){
	let chrCount = printChr(value) + 1;
	putLn();
	return chrCount;
}

// Print a string and return the number of printed characters.
func printStr(value){
	let mut position = value;
	let mut character = *position;
	
	while(character){
		putChr(character);
		character = *(position += 1);
	}
	
	return position - value;
}

/*
* Print a string with a line break and return the number of printed
* characters.
*/
func printStrLn(value){
	let chrCount = printStr(value) + 1;
	putLn();
	return chrCount;
}

// Return the length of a string excluding the null terminator.
func lenStr(string){
	let mut position = string;
	let mut character = *position;
	
	while(character){
		character = *(position += 1);
	}
	
	return position - string;
}

/*
* Compare two strings as greater (> 0), lesser (< 0), or equal (== 0) when
* sorted lexically.
*/
func cmpStr(mut x, mut y){
	let mut chrX = *x;
	let mut chrY = *y;
	
	while(chrX & chrX == chrY){
		chrX = *(x += 1);
		chrY = *(y += 1);
	}
	
	return chrX - chrY;
}

// Return whether two strings are equal.
func eqStr(x, y){
	return !cmpStr(x, y);
}
