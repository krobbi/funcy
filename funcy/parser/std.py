FUNCY_STANDARD_LIBRARY: str = """/*
* Funcy Standard Library
* A library of functions intrinsic to all Funcy programs.
*/

// Return an integer's absolute value.
func abs(value){
    if(value < 0){
        return -value;
    }else{
        return value;
    }
}

// Return an integer's sign.
func sign(value){
    return (value > 0) - (value < 0);
}

// Return the smallest of two integers.
func min(x, y){
    if(x < y){
        return x;
    } else {
        return y;
    }
}

// Return the largest of two integers.
func max(x, y){
    if(x > y){
        return x;
    } else {
        return y;
    }
}

// Put and return a character.
func putChr(character){
    return $(putChr, character);
}

// Put and return a line break.
func putLn(){
    return $(putChr, '\\n');
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
        $(putChr, '-');
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
        $(putChr, getDigitChr(digit));
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
    $(putChr, '\\n');
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
    $(putChr, '\\n');
    return chrCount;
}

// Print a character and return the number of printed characters.
func printChr(value){
    if(value){
        $(putChr, value);
        return 1;
    }
    
    return 0;
}

/*
* Print a character with a line break and return the number of printed
* characters.
*/
func printChrLn(value){
    if(value){
        $(putChr, value);
        $(putChr, '\\n');
        return 2;
    }
    
    $(putChr, '\\n');
    return 1;
}

// Print a string and return the number of printed characters.
func printStr(value){
    let mut position = value;
    let mut character = *position;
    
    while(character){
        $(putChr, character);
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
    $(putChr, '\\n');
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

// Compare two strings as greater, lesser or equal.
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

// DEPRECATED: Use 'printIntLn' instead!
func print(value){
    printStrLn("Function 'print' is deprecated! Use 'printIntLn' instead.");
    return printIntLn(value);
}
"""
""" The Funcy Standard Library's source code. """
