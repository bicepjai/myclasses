#include <iostream>
// #include <ctime>
using namespace std;
typedef long long ull;
typedef unsigned long long uull;

ull gcdIter(ull a, ull b) {
   if (b == 0) return a;
   else return gcdIter(b, a % b);
}

ull gcd(ull a, ull b) {
   if (b == 0 || a == 0) return 1;
   else return gcdIter(a, b);
}

ull lcmFast(ull a, ull b) {
   return (a * b)/gcd(a,b);
}

int main() {

   // int start_s = 0;
   // int stop_s = 0;
   // while (true) {
   //    ull a = rand() % 2000000000;
   //    ull b = rand() % 2000000000;
   //    cout << a << " " << b << "\n";

   //    start_s = clock();
   //    long long res1 = lcmFast(a, b);
   //    stop_s = clock();
   //    cout << "lcm:" << res1 << " time: " << (stop_s - start_s) / double(CLOCKS_PER_SEC) * 1000 << " ms" << endl;

   //    start_s = clock();
   //    long long res2 = lcmFast(a, b);
   //    stop_s = clock();
   //    cout << "lcmFast:" << res2 << " time: " << (stop_s - start_s) / double(CLOCKS_PER_SEC) * 1000 << " ms" << endl;

   //    if (res1 != res2) {
   //       cout << "Wrong answer: " << res1 << ' ' << res2 << "\n";
   //       getchar();
   //       // break;
   //    }
   //    else {
   //       cout << "OK\n";
   //    }

   //    cout << "\n";
   //    // getchar();
   // }


   // Submission program starts here
   ull a, b;
   cin >> a;
   cin >> b;

   ull result = lcmFast(a , b);
   cout << result;
   return 0;
}

