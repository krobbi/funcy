/*
* Funcy Standard Library
* A library of all available standard functions.
*/

include "//math.fy";
include "//print.fy";

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
