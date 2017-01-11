#include <iostream>
// #include <ctime>
using namespace std;
typedef long long ull;

ull fib_array[10000009];

ull calcFibModm(ull n, ull m) {
  fib_array[0] = 0;
  fib_array[1] = 1;
  for (ull i = 2; i <= n; i++)
    fib_array[i] = (fib_array[i - 1] + fib_array[i - 2]) % m;
  return fib_array[n];
}


ull calcFibModmFast(ull n, ull m) {
   fib_array[0] = 0;
   fib_array[1] = 1;
   ull pp = 0; //pisano period
   for (pp = 2; pp <= n+m; pp++){
      fib_array[pp] = (fib_array[pp - 1] + fib_array[pp - 2]) % m;
      // break when teh pattern 0,1 is seen
      if (fib_array[pp-1] % m == 0 && fib_array[pp] % m == 1) break;
   }
   // moved one element over for checking pattern 0,1
   pp--;

   return fib_array[n%pp];
}

int main() {

   // ull start_s = 0;
   // ull stop_s = 0;
   // while (true) {
   //    ull n = rand() % 10000000000; //1000000000000000009;
   //    ull m = rand() % 100000;
   //    cout << n << " " << m << "\n";

   //    start_s = clock();
   //    ull res1 = calcFibModm(n, m);
   //    stop_s = clock();
   //    cout << "calcFibModm:" << res1 << " time: " << (stop_s - start_s) / double(CLOCKS_PER_SEC) * 1000 << " ms" << endl;

   //   start_s = clock();
   //    ull res2 = calcFibModmFast(n, m);
   //    stop_s = clock();
   //    cout << "calcFibModmFast:" << res2 << " time: " << (stop_s - start_s) / double(CLOCKS_PER_SEC) * 1000 << " ms" << endl;

   //     if (res1 != res2) {
   //       cout << "Wrong answer: " << res1 << ' ' << res2 << "\n";
   //       getchar();
   //       // break;
   //     }
   //     else {
   //       cout << "OK\n";
   //     }

   //    cout << "\n";
   //    // getchar();
   // }


   // Submission program starts here
   ull n, m;
   cin >> n >> m;
   ull result = calcFibModmFast(n, m);
   cout << result << endl;
   return 0;
}
