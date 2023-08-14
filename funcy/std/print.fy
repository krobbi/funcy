/*
* Funcy Print Library
* A library of functions for printing values.
*/

include "intrinsics:chrAt";
include "intrinsics:putChr";

// Get a digit's character. E.g. 5 -> '5', 10 -> 'a'.
func getDigitChr(digit) {
	if (digit < 10) {
		return digit + '0';
	} else {
		return digit + 'a' - 10;
	}
}

// Print a string.
func printStr(string) {
	let mut index = 0;
	let mut character = chrAt(string, index);
	
	while(character) {
		putChr(character);
		character = chrAt(string, index += 1);
	}
}

// Print a string with a line break.
func printStrLn(string) {
	printStr(string);
	putChr('\n');
}

// Print an integer with a base between 2 and 36.
func printIntBase(mut value, base){
	if (base < 2 | base > 36) {
		return;
	}
	
	if (value < 0) {
		value = -value;
		putChr('-');
	}
	
	let mut magnitude = base;
	
	while (magnitude <= value) {
		magnitude *= base;
	}
	
	while (magnitude >= base) {
		magnitude /= base;
		let digit = value / magnitude;
		value -= digit * magnitude;
		putChr(getDigitChr(digit));
	}
}

// Print an integer with a base between 2 and 36 with a line break.
func printIntBaseLn(value, base) {
	printIntBase(value, base);
	putChr('\n');
}

// Print an integer.
func printInt(value) {
	printIntBase(value, 10);
}

// Print an integer with a line break.
func printIntLn(value) {
	printIntBase(value, 10);
	putChr('\n');
}
