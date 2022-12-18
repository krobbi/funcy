/*
* Funcy Print Library
* A library of functions for printing values.
*/

// Get a digit's character. E.g. 5 -> '5', 10 -> 'a'.
func getDigitChr(digit){
	if(digit < 10){
		return digit + '0';
	} else {
		return digit + 'a' - 10;
	}
}

// Put a character to the standard output and return it.
func putChr(character){
	return $(putChr, character);
}

// Put a line break to the standard output and return it.
func putLn(){
	return putChr('\n');
}

// Print a line break and return the number of printed characters.
func printLn(){
	putLn();
	return 1;
}

// Print a character and return the number of printed characters.
func printChr(character){
	if(character){
		putChr(character);
		return 1;
	} else {
		return 0;
	}
}

/*
* Print a character with a line break and return the number of printed
* characters.
*/
func printChrLn(character){
	return printChr(character) + printLn();
}

// Print a string and return the number of printed characters.
func printStr(string){
	let mut index = string;
	let mut character = *string;
	
	while(character){
		putChr(character);
		character = *(index += 1);
	}
	
	return index - string;
}

// Print a string with a line break and return the number of printed characters.
func printStrLn(string){
	return printStr(string) + printLn();
}

/*
* Print an integer with a base between 2 and 36 and return the number of printed
* characters.
*/
func printIntBase(mut value, base){
	if(base < 2 | base > 36){
		return 0;
	}
	
	let mut chrCount = 0;
	
	if(value < 0){
		value = -value;
		chrCount = printChr('-');
	}
	
	let mut magnitude = base;
	
	while(magnitude <= value){
		magnitude *= base;
	}
	
	while(magnitude >= base){
		magnitude /= base;
		let digit = value / magnitude;
		value -= digit * magnitude;
		chrCount += printChr(getDigitChr(digit));
	}
	
	return chrCount;
}

/*
* Print an integer with a base between 2 and 36 and a line break and return the
* number of printed characters.
*/
func printIntBaseLn(value, base){
	return printIntBase(value, base) + printLn();
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
	return printInt(value) + printLn();
}
