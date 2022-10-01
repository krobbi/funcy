/*
* Funcy Test Script - example.fy
* Calculates squared distances between 2D points.
*/

// Calculate the distance squared between (aX, aY) and (bX, bY).
func distanceSquared2D(aX, aY, bX, bY){
   // Return x squared.
   func sq(x){
      return x * x;
   }
   
   return sq(bX - aX) + sq(bY - aY);
}

// Entry point.
func main(){
   // Test the distance function and return whether it failed.
   func testFailed(aX, aY, bX, bY, result){
      return distanceSquared2D(aX, aY, bX, bY) != result;
   }
   
   // Run tests on our squared distance function:
   if(testFailed(0, 0, 0, 0, 0)) return 1;
   if(testFailed(123, 456, 123, 456, 0)) return 1;
   if(testFailed(0, 0, 1, 0, 1)) return 1;
   if(testFailed(0, 0, 1, 1, 2)) return 1;
   if(testFailed(0, 0, 10, 0, 100)) return 1;
   if(testFailed(5, 10, 15, 10, 100)) return 1;
   if(testFailed(2, 3, 5, 7, 25)) return 1;
   if(testFailed(0, 10, 0, -10, 400)) return 1;
   
   printIntLn(123); // Print 123 on success!
}
