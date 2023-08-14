/*
* Funcy Test Script - intrinsics.fy
* Calls all intrinsic functions.
*/

include "intrinsics:chrAt";
include "intrinsics:putChr";

// Call a function with an argument.
func call(f, x) {
	return f(x);
}

// Call all intrinisc functions.
func main() {
	putChr('A'); // Calling an intrinsic directly should inline it.
	call(putChr, 'B'); // But a true function is also generated.
	putChr(chrAt("Hi!", 2));
	putChr('\n');
}
