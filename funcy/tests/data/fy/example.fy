/*
* Funcy Test Script - example.fy
* Calculates the distance squared between (2, 3) and (5, 7)
*/

// Calculate the distance squared between (aX, aY) and (bX, bY).
func distanceSquared2D(aX, aY, bX, bY){
   // Return x squared.
   func sq(x){
      return x * x;
   }
   
   return sq(bX - aX) + sq(bY - aY);
}

// Print the distance squared between (2, 3) and (5, 7).
func main(){
   print(distanceSquared2D(2, 3, 5, 7)); // Should be '25'.
}
