#include <iostream>
// #include <ctime>
using namespace std;
typedef long long ll;


// ll gcd(ll a, ll b) {
//    //write your code here
//    ll current_gcd = 1;
//    for (ll d = 2; d <= a && d <= b; d++) {
//       if (a % d == 0 && b % d == 0) {
//          if (d > current_gcd) {
//             current_gcd = d;
//          }
//       }
//    }
//    return current_gcd;
// }

ll gcdFastIter(ll a, ll b) {
   if (b == 0) return a;
   else return gcdFastIter(b, a % b);
}

ll gcdFast(ll a, ll b) {
   if (b == 0 || a == 0) return 1;
   else return gcdFastIter(a, b);
}

int main() {

   // int start_s = 0;
   // int stop_s = 0;
   // while (true) {
   //    ll a = rand() % 2000000000;
   //    ll b = rand() % 2000000000;
   //    cout << a << " " << b << "\n";

   //    start_s = clock();
   //    long long res1 = gcd(a, b);
   //    stop_s = clock();
   //    cout << "gcd:" << res1 << " time: " << (stop_s - start_s) / double(CLOCKS_PER_SEC) * 1000 << " ms" << endl;

   //    start_s = clock();
   //    long long res2 = gcdFast(a, b);
   //    stop_s = clock();
   //    cout << "gcdFast:" << res2 << " time: " << (stop_s - start_s) / double(CLOCKS_PER_SEC) * 1000 << " ms" << endl;

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
   ll a, b;
   cin >> a;
   cin >> b;

   ll result = gcdFast(a , b);
   cout << result;
   return 0;
}
