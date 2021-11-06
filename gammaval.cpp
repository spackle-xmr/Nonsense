#include <iostream>
#include <random>

int main()
{
  std::mt19937 rng(std::random_device{}());
  rng.discard(700000);
  std::uniform_int_distribution<> window50(11, 50); // define the range
  std::gamma_distribution<double> distribution(19.28,(1/1.61));

  double number = distribution(rng);
  while (number > 15.5){
    number = distribution(rng);
  }
  number = exp(number); //decoy target age in seconds
  number = number / 120; //decoy target relative block index
  number = round(number);
  
  if(number < 10){ // #7821
    number = window50(rng);
  }
  //core useful code
    //int timerval = (int) number;
    std::cout << number << std::endl;
  return 0;
}
