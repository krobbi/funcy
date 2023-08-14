/*
* Funcy String Library
* A library of functions for string manipulation.
*/

include "intrinsics:chrAt";

// Return the length of a string.
func strLen(string) {
	let mut index = -1;
	
	while (chrAt(string, index += 1)) {
		;
	}
	
	return index;
}

// Compare two strings as greater (1), lesser (-1), or equal (0) when sorted
// lexically.
func strCmp(x, y) {
	if (x == y) {
		return 0;
	}
	
	let mut index = 0;
	let mut characterX = chrAt(x, index);
	let mut characterY = chrAt(y, index);
	
	while(characterX & characterX == characterY){
		index += 1;
		characterX = chrAt(x, index);
		characterY = chrAt(y, index);
	}
	
	return (characterX > characterY) - (characterX < characterY);
}

// Return whether two strings are equal by value.
func strEq(x, y) {
	return !strCmp(x, y);
}
