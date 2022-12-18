/*
* Funcy String Library
* A library of functions for string manipulation.
*/

// Return the length of a string excluding its null terminator.
func strLen(string){
	let mut index = string;
	let mut character = *string;
	
	while(character){
		character = *(index += 1);
	}
	
	return index - string;
}

/*
* Compare to strings as greater (1), lesser (-1), or equal (0) when sorted
* lexically.
*/
func strCmp(mut x, mut y){
	if(x == y){
		return 0;
	}
	
	let mut characterX = *x;
	let mut characterY = *y;
	
	while(characterX & characterX == characterY){
		characterX = *(x += 1);
		characterY = *(y += 1);
	}
	
	return (characterX > characterY) - (characterX < characterY);
}

// Return whether two strings are equal by value.
func strEq(x, y){
	return !strCmp(x, y);
}
