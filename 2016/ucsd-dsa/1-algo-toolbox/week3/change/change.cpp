#include <iostream>
// #include <ctime>
using namespace std;
typedef long long ull;

ull GetChange(ull n) {
  //write your code here
   ull change = 0;
   ull remainder = 0;

   change = n/10;
   // cout << change << " ";
   remainder = n%10;

   change += remainder/5;
   // cout << remainder/5 << " ";

   remainder = remainder%5;

   change += remainder;
   // cout << remainder << " ";

  return change;
}

int main() {
   // ull start_s = 0;
   // ull stop_s = 0;
   // while (true) {
   //    ull n = rand() % 1000; //1000000000000000009;
   //    cout << n << " \n";

   //    start_s = clock();
   //    ull res1 = GetChange(n);
   //    stop_s = clock();
   //    cout << "GetChange:" << res1 << " time: " << (stop_s - start_s) / double(CLOCKS_PER_SEC) * 1000 << " ms" << endl;

   //    cout << "\n";
   //    // getchar();
   // }

  ull n;
  std::cin >> n;
  std::cout << GetChange(n) << '\n';
}

