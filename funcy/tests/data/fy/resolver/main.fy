include "//std.fy";

include "foo.fy";
include "bar.fy";

func main(){
	printStrLn(getFoo());
	printStrLn(getBar());
}
