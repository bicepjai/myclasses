#include <iostream>
// #include <ctime>
using namespace std;
typedef long long ll;

// long long calcFib(int n) {
//    long long fib_array[100];
//    fib_array[0] = 0;
//    fib_array[1] = 1;
//    for(int i=2; i<=n; i++)
//       fib_array[i] = fib_array[i-1] + fib_array[i-2];
//    return fib_array[n] % 10;
// }

ll fib_array[10000009];
ll calcFibLastDigitFast(ll n) {
  fib_array[0] = 0;
  fib_array[1] = 1;
  for (ll i = 2; i <= n; i++)
    fib_array[i] = (fib_array[i - 1] + fib_array[i - 2]) % 10;
  return fib_array[n];
}

int main() {

  //  int start_s = 0;
  //  int stop_s = 0;
  //  while (true) {
  //     int n = rand() % 45;
  //     cout << n << "\n";

  //     start_s=clock();
  //     long long res1 = calcFib(n);
  //     stop_s=clock();
  //     cout << "calcFib:" << res1 << " time: " <<(stop_s-start_s)/double(CLOCKS_PER_SEC)*1000 << " ms"<< endl;

  //     start_s=clock();
  //     long long res2 = calcFibLastDigitFast(n);
  //     stop_s=clock();
  //     cout << "calcFibLastDigitFast:" << res2 << " time: " <<(stop_s-start_s)/double(CLOCKS_PER_SEC)*1000 << " ms"<< endl;

  //      if (res1 != res2) {
  //        cout << "Wrong answer: " << res1 << ' ' << res2 << "\n";
  //        // getchar();
  //        break;
  //      }
  //      else {
  //        cout << "OK\n";
  //      }

  //     cout << "\n";
  //     // getchar();
  // }


  // Submission program starts here
  ll n;
  cin >> n;
  ll result = calcFibLastDigitFast(n);
  cout << result;
  return 0;
}
