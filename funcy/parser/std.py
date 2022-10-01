FUNCY_STANDARD_LIBRARY: str = """/*
* Funcy Standard Library
* A library of functions intrinsic to all Funcy programs.
*/

// Put and return a character.
func putChr(character){
    return $(putChr, character);
}

// Put and return a line break.
func putLn(){
    return putChr(0x0a); // '\\n'.
}

// Get a digit's character. E.g. 5 -> '5', 10 -> 'a'.
func getDigitChr(digit){
    if(digit < 10){
        return digit + 0x30; // digit + '0'.
    } else {
        return digit + 0x57; // digit + 'a' - 10.
    }
}

/*
* Print an integer value with a base between 2 and 36 and return the
* number of printed characters.
*/
func printIntBase(mut value, base){
    if(base < 2 | base > 36){
        return 0;
    }
    
    let mut chrCount = 0; // Number of printed characters.
    
    if(value < 0){
        value = -value;
        putChr(0x2d); // '-'.
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
* Print an integer value with a base between 2 and 36 and a line break
* and return the number of printed characters.
*/
func printIntBaseLn(value, base){
    let chrCount = printIntBase(value, base);
    putLn();
    return chrCount + 1;
}

// Print an integer value and return the number of printed characters.
func printInt(value){
    return printIntBase(value, 10);
}

/*
* Print an integer value with a line break and return the number of
* printed characters.
*/
func printIntLn(value){
    return printIntBaseLn(value, 10);
}

// DEPRECATED: Use 'printIntLn' instead!
func print(value){
    return printIntLn(value);
}
"""
""" The Funcy Standard Library's source code. """
