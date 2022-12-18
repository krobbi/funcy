/*
* Funcy Math Library
* A library of mathematical functions for Funcy programs.
*/

// Return an integer's absolute value.
func abs(value){
	if(value < 0){
		return -value;
	} else {
		return value;
	}
}

// Return an integer's sign as zero (0), positive (1), or negative (-1).
func sign(value){
	return (value > 0) - (value < 0);
}

// Return the minimum of two integers.
func min(x, y){
	if(x < y){
		return x;
	} else {
		return y;
	}
}

// Return the maximum of two integers.
func max(x, y){
	if(x > y){
		return x;
	} else {
		return y;
	}
}
